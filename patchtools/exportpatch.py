"""
Export patches from upstream, in SUSE format.

Export one or more patches from a repository with the SUSE set of patch headers.
"""

__author__ = 'Jeff Mahoney'

import os
import sys
from optparse import OptionParser
from pathlib import Path

from patchtools import PatchError
from patchtools import __version__ as patchtools_version
from patchtools.patch import EmptyCommitError, Patch

WRITE_PATCHFILE_DEFAULT = False
WRITE_PATCHFILE_DIR_DEFAULT = '.'

def export_patch(commit, options, prefix, suffix):
    try:
        p = Patch(commit, debug=options.debug, force=options.force)
    except PatchError as e:
        print(e, file=sys.stderr)
        return 0
    if p.find_commit():
        if options.reference:
            p.add_references(options.reference)
        if options.extract:
            try:
                p.filter(options.extract)
            except EmptyCommitError:
                print(f'Commit {commit} is now empty. Skipping.', file=sys.stderr)
                return 0
        if options.exclude:
            try:
                p.filter(options.exclude, True)
            except EmptyCommitError:
                print(f'Commit {commit} is now empty. Skipping.', file=sys.stderr)
                return 0
        p.add_signature(options.signed_off_by)
        if options.write:
            fn = p.get_pathname(options.dir, prefix, suffix)
            if os.path.exists(fn) and not options.force:
                f = fn
                fn += f'-{commit[0:8]}'
                print(f'{f} already exists. Using {fn}', file=sys.stderr)
            print(os.path.basename(fn))
            try:
                with Path(fn).open('w') as f:
                    print(p.message.as_string(False), file=f)
            except Exception as e:
                print(f'Failed to write {fn}: {e}', file=sys.stderr)
                raise e
        else:
            print(p.message.as_string(False))
        return 0

    print(f'Could not locate commit "{commit}"; Skipping.', file=sys.stderr)
    return 1

def main():
    """Export one or more patches from git, by commit hash"""
    parser = OptionParser(version='%prog ' + patchtools_version,
                          usage='%prog [options] <LIST OF COMMIT HASHES> --  export patch with proper patch headers')
    parser.add_option('-w', '--write', action='store_true',
                      help='write patch file(s) instead of stdout [default is %default]',
                      default=WRITE_PATCHFILE_DEFAULT)
    parser.add_option('-s', '--suffix', action='store_true',
                      help='when used with -w, append .patch suffix to filenames.',
                      default=False)
    parser.add_option('-n', '--numeric', action='store_true',
                      help='when used with -w, prepend order numbers to filenames.',
                      default=False)
    parser.add_option('--num-width', type='int', action='store',
                      help='when used with -n, set the width of the order numbers',
                      default=4)
    parser.add_option('-N', '--first-number', action='store',
                      help='Start numbering the patches with number instead of 1',
                      default=1)
    parser.add_option('-d', '--dir', action='store',
                      help="write patch to this directory (default '.')",
                      default=WRITE_PATCHFILE_DIR_DEFAULT)
    parser.add_option('-f', '--force', action='store_true',
                      help='write over existing patch or export commit that only exists in local repo',
                      default=False)
    parser.add_option('-D', '--debug', action='store_true',
                      help='set debug mode', default=False)
    parser.add_option('-F', '--reference', action='append',
                      help='add reference tag. This option can be specified multiple times.',
                      default=None)
    parser.add_option('-x', '--extract', action='append',
                      help='extract specific parts of the commit; using a path that ends with / includes all files under that hierarchy. This option can be specified multiple times.',
                      default=None)
    parser.add_option('-X', '--exclude', action='append',
                      help='exclude specific parts of the commit; using a path that ends with / excludes all files under that hierarchy. This option can be specified multiple times.',
                      default=None)
    parser.add_option('-S', '--signed-off-by', action='store_true',
                      default=False,
                      help='Use Signed-off-by instead of Acked-by')
    (options, args) = parser.parse_args()

    if not args:
        parser.error('Must supply patch hash(es)')
        return 1

    try:
        n = int(options.first_number)
    except ValueError:
        print('option -N needs a number')
        return 1

    max_val=9999
    if n + len(args) > max_val or n < 0:
        print(f'The starting number + commits needs to be in the range 0 - {max_val}')
        return 1

    suffix = '.patch' if options.suffix else ''

    num_width = 4
    max_width = 5
    if options.num_width:
        _n = int(options.num_width)
        if _n > 0 and _n < max_width:
            num_width = _n

    for commit in args:
        prefix = '{0:0{1}}-'.format(n, num_width) if options.numeric else ''

        res = export_patch(commit, options, prefix, suffix)
        if res != 0:
            return res
        n += 1

    return 0

# vim: sw=4 ts=4 et si:
