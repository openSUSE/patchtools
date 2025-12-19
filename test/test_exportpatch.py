#!/usr/bin/python3.11
"""The test suite for the patchtools exportpatch command."""

import filecmp
import tempfile
import unittest
from pathlib import Path
from subprocess import PIPE, run


def my_run_command(command, stdin=None, our_input=None, stdout=PIPE, cwd=None):
    """Run the specified command."""
    with Path('/dev/null').open('wb') as dn:
        proc = run(command.split(), encoding='utf-8', check=False, cwd=cwd,
                   stdin=stdin, input=our_input, stdout=stdout, stderr=dn)
        return (proc.returncode, proc.stdout)


def get_patch_path(fname, dirname=None, prefix='', suffix='', truncate=64):
    """Return a patch filename that isn't too long"""
    truncate_chars = truncate - len(fname) - len(prefix + suffix)
    if truncate_chars < 0:
        fname = fname[0:truncate_chars]
    fpath = Path(prefix + fname + suffix)
    if dirname:
        fpath = Path(dirname) / fpath
    return fpath


# the command we are here to test
test_cmd = 'exportpatch'

# a known commit we use for simple tests
known_st_commit = '8db816c6f176321e42254badd5c1a8df8bfcfdb4'

# the base patch name for our known st commit (no suffix, etc)
known_st_patch = 'scsi-st-Tighten-the-page-format-heuristics-with-MODE-SELECT'


class TestExportpatchNormalFunctionality(unittest.TestCase):

    def test_output_to_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # make sure our output file doesn't exist (even though its a temp dir)
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir)
            ofile_path.unlink(missing_ok=True)
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -d {tmpdir} {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

            # test same thing but with suffix
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir, suffix='.patch')
            ofile_path.unlink(missing_ok=True)
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -s -d {tmpdir} {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')


if __name__ == '__main__':
    unittest.main()
