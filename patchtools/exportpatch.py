"""Export a patch from a repository with the SUSE set of patch headers.

From Jeff Mahoney, updated by Lee Duncan.
"""

__revision__ = 'Revision: 2.5'
__author__ = 'Jeff Mahoney'

import sys
from patchtools import PatchException
from patchtools.modified_optparse import ModifiedOptionParser, OptionParsingError
from patchtools.patch import Patch, EmptyCommitException
import os


# default: do not write out a patch file
WRITE=False

# default directory where patch gets written
DIR="."


def export_patch(commit, options, prefix, suffix):
    """Export a single commit/patch. Return 0 for success, else 1."""
    try:
        p = Patch(commit, debug=options.debug, force=options.force)
    except PatchException as e:
        print(e, file=sys.stderr)
        return 1
    if p.find_commit():
        if options.reference:
            p.add_references(options.reference)
        if options.extract:
            try:
                p.filter(options.extract)
            except EmptyCommitException:
                print("Commit %s is now empty. Skipping." % commit, file=sys.stderr)
                return 0
        if options.exclude:
            try:
                p.filter(options.exclude, True)
            except EmptyCommitException:
                print("Commit %s is now empty. Skipping." % commit, file=sys.stderr)
                return 0
        p.add_signature(options.signed_off_by)
        if options.write:
            fn = p.get_pathname(options.dir, prefix, suffix)
            if os.path.exists(fn) and not options.force:
                f = fn
                fn += "-%s" % commit[0:8]
                print("%s already exists. Using %s" % (f, fn), file=sys.stderr)
            print(os.path.basename(fn))
            try:
                f = open(fn, "w")
            except OSError as e:
                print(e, file=sys.stderr)
                return 1

            print(p.message.as_string(False), file=f)
            f.close()
        else:
            print(p.message.as_string(False))
        return 0

    print("Couldn't locate commit \"%s\"; Skipping." % commit, file=sys.stderr)
    return 1


def main():
    """The main entry point for this module. Return 0 for success."""
    parser = ModifiedOptionParser(
                version='%prog ' + __revision__,
                usage='%prog [options] <LIST OF COMMIT HASHES> --  export patch with proper patch headers')
    parser.add_option("-w", "--write", action="store_true",
                      help="write patch file(s) instead of stdout [default is %default]",
                      default=WRITE)
    parser.add_option("-s", "--suffix", action="store_true",
                      help="when used with -w, append .patch suffix to filenames.",
                      default=False)
    parser.add_option("-n", "--numeric", action="store_true",
                      help="when used with -w, prepend order numbers to filenames.",
                      default=False)
    parser.add_option("--num-width", type="int", action="store",
                      help="when used with -n, set the width of the order numbers",
                      default=4)
    parser.add_option("-N", "--first-number", type="int", action="store",
                      help="Start numbering the patches with number instead of 1",
                      default=1)
    parser.add_option("-d", "--dir", action="store",
                      help="write patch to this directory (default '.')", default=DIR)
    parser.add_option("-f", "--force", action="store_true",
                      help="write over existing patch or export commit that only exists in local repo", default=False)
    parser.add_option("-D", "--debug", action="store_true",
                      help="set debug mode", default=False)
    parser.add_option("-F", "--reference", action="append",
                      help="add reference tag. This option can be specified multiple times.", default=None)
    parser.add_option("-x", "--extract", action="append",
                      help="extract specific parts of the commit; using a path that ends with / includes all files under that hierarchy. This option can be specified multiple times.", default=None)
    parser.add_option("-X", "--exclude", action="append",
                      help="exclude specific parts of the commit; using a path that ends with / excludes all files under that hierarchy. This option can be specified multiple times.", default=None)
    parser.add_option("-S", "--signed-off-by", action="store_true",
                      default=False,
                      help="Use Signed-off-by instead of Acked-by")

    try:
        (options, args) = parser.parse_args()

    except OptionParsingError as e:
        print(f'Option paring error: {e.msg}', file=sys.stderr)
        return 1

    if not args:
        print("Must supply patch hash(es)", file=sys.stderr)
        return 1

    if options.first_number + len(args) > 9999 or options.first_number < 0:
        print("The starting number + commits needs to be in the range 0 - 9999",
              file=sys.stderr)
        return 1

    suffix = ""
    if options.suffix:
        suffix = ".patch"

    num_width = 4
    if options.num_width:
        _n = int(options.num_width)
        if _n > 0 and _n < 5:
            num_width = _n

    n = options.first_number
    for commit in args:
        prefix = ""
        if options.numeric:
            prefix = "{0:0{1}}-".format(n, num_width)

        res = export_patch(commit, options, prefix, suffix)
        if res:
            return res

        n += 1

    return 0

# vim: sw=4 ts=4 et si:
