"""Fix an existing patch with the proper tags.

Take an existing patch and add the appropriate tags, drawing from known
repositories to discover the origin. Also, renames the patch using the
subject found in the patch itself.
"""

__revision__ = 'Revision: 2.5'
__author__ = 'Jeff Mahoney'


from patchtools import PatchException
from patchtools.patch import Patch
from optparse import OptionParser
import sys
import os


def process_file(pathname, options):
    """Fix one patchfile. Return 0 for success."""
    try:
        p = Patch()
        f = open(pathname, "r")
        p.from_email(f.read())

        if options.name_only:
            suffix=""
            if options.suffix:
                suffix = ".patch"
            fn = p.get_pathname()
            print("{}{}".format(fn, suffix))
            return 0

        if options.update_only:
            options.header_only = True
            options.no_rename = True

        if options.header_only:
            options.no_ack = True
            options.no_diffstat = True
            if options.reference:
                print("References won't be updated in header-only mode.", file=sys.stderr)
                options.reference = None

        if not options.no_diffstat:
            p.add_diffstat()
        if not options.no_ack:
            p.add_signature(options.signed_off_by)

        if options.reference:
            p.add_references(options.reference)

        if options.mainline:
            p.add_mainline(options.mainline)

        if options.dry_run:
            print(p.message.as_string(unixfrom=False))
            return 0

        suffix=""
        if options.suffix:
            suffix = ".patch"

        if options.no_rename:
            fn = pathname
        else:
            fn = "{}{}".format(p.get_pathname(), suffix)
            dirname = os.path.dirname(pathname)
            if dirname != '':
                fn = "{}/{}".format(dirname, fn)
            if fn != pathname and os.path.exists(fn) and not options.force:
                print("%s already exists." % fn, file=sys.stderr)
                return 1
        f = open(fn, "w")
        print(fn)
        print(p.message.as_string(unixfrom=False), file=f)
        f.close()
        if fn != pathname:
            os.unlink(pathname)

    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    except PermissionError as e:
        print(e, file=sys.stderr)
        return 1

    except PatchException as e:
        print(e, file=sys.stderr)
        return 1

    return 0

#
# set up Option Parsing class so that we can
# stop the option parser from calling sys.exit()
# when it encounters an error
#

class OptionParsingError(RuntimeError):
    """An exception raised when parser.error() is called."""
    def __init__(self, msg):
        self.msg = msg

class ModifiedOptionParser(OptionParser):
    """Our own Option Parsing class, that does not call sys.exit()."""
    def error(self, msg):
        raise OptionParsingError(msg)


def main():
    """The main entry point for this module. Return 0 for success."""
    parser = ModifiedOptionParser(\
            version='%prog ' + __revision__,
            usage='%prog [options] <LIST OF PATCH FILES TO FIX> -- fix patch files with proper headers')
    parser.add_option("-n", "--dry-run", action="store_true", default=False,
                      help="Output results to stdout but don't commit change")
    parser.add_option("-N", "--no-ack", action="store_true", default=False,
                      help="Don't add Acked-by tag (will add by default)")
    parser.add_option("-D", "--no-diffstat", action="store_true", default=False,
                      help="Don't add the diffstat to the patch")
    parser.add_option("-r", "--no-rename", action="store_true", default=False,
                      help="Don't rename the patch")
    parser.add_option("-f", "--force", action="store_true", default=False,
                      help="Overwrite patch if it exists already")
    parser.add_option("-H", "--header-only", action="store_true", default=False,
                      help="Only update patch headers, don't do Acked-by, diffstat, or add references")
    parser.add_option("-U", "--update-only", action="store_true", default=False,
                      help="Update the patch headers but don't rename (-Hr)")
    parser.add_option("-R", "--name-only", action="store_true", default=False,
                      help="Print the new filename for the patch but don't change anything")
    parser.add_option("-F", "--reference", action="append", default=None,
                      help="add reference tag, if not in header-only mode. Can be supplied multiple times.")
    parser.add_option("-S", "--signed-off-by", action="store_true", default=False,
                      help="Use Signed-off-by instead of Acked-by")
    parser.add_option("-M", "--mainline", action="append", default=None,
                      help="Add dummy Patch-mainline tag. Can be supplied multiple times.")
    parser.add_option("-s", "--suffix", action="store_true",
                      help='When generating the patch name, append ".patch"',
                      default=False)

    try:
        (options, args) = parser.parse_args()

    except OptionParsingError as e:
        print(f'Option paring error: {e.msg}', file=sys.stderr)
        return 1

    if not args:
        print("Must supply patch filename(s)", file=sys.stderr)
        return 1

    for pathname in args:
        res = process_file(pathname, options)
        if res:
            return 1

    return 0

# vim: sw=4 ts=4 et si:
