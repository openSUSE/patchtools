#!/usr/bin/python3.11
"""The test suite for the patchtools exportpatch command.

Test using the locally available 'exportpatch' command, and its
libraries. Assume the local config files are correct."""

import os
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

def debug_dump_file(fname):
    print(f'DEBUG: dumping file: {fname} ...')
    with Path(fname).open(encoding='utf-8') as f:
        for aline in f:
            print(aline.rstrip())

# the command we are here to test
test_cmd = 'exportpatch'

# a known commit we use for simple tests
known_st_commit = '8db816c6f176321e42254badd5c1a8df8bfcfdb4'

# the base patch name for our known st commit (no suffix, etc)
known_st_patch = 'scsi-st-Tighten-the-page-format-heuristics-with-MODE-SELECT'


class TestExportpatchNormalFunctionality(unittest.TestCase):
    """Test normal functionality for 'exportpatch'"""

    def test_to_file_in_dir_defaults(self):
        """Test exportpatch to file/dir, using default arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir)
            # make sure our output file doesn't exist (even though its a temp dir)
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

    def test_to_file_in_dir_suffix(self):
        """Test exportpatch to file/dir, with a suffix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir, suffix='.patch')
            # make sure our output file doesn't exist (even though its a temp dir)
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

    def test_to_file_in_dir_numeric_default(self):
        """Test exportpatch to file/dir, with numeric filename, using default start"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir, prefix='0001-')
            # make sure our output file doesn't exist (even though its a temp dir)
            ofile_path.unlink(missing_ok=True)
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -d {tmpdir} -n {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_dir_numeric_s2(self):
        """Test exportpatch to file/dir, with numeric filename, using start number 2"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # make sure our output file doesn't exist (even though its a temp dir)
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir, prefix='0002-')
            ofile_path.unlink(missing_ok=True)
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -d {tmpdir} -n -N 2 {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_dir_numeric_w3(self):
        """Test exportpatch to file/dir, with numeric filename, using width of 3"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir, prefix='001-')
            # make sure our output file doesn't exist (even though its a temp dir)
            ofile_path.unlink(missing_ok=True)
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -d {tmpdir} -n --num-width 3 {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_dir_overwrite_force(self):
        """Test exportpatch to file/dir, where patch already exists, using overwrite"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir)
            # make sure our output file doesn't exist, then create empty one
            ofile_path.unlink(missing_ok=True)
            ofile_path.touch()
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -d {tmpdir} -f {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_dir_overwrite_no_force(self):
        """Test exportpatch to file/dir, where patch already exists, not using overwrite"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir)
            # make sure our output file doesn't exist, then create empty one
            ofile_path.unlink(missing_ok=True)
            ofile_path.touch()
            # now set up path for patch name expected
            ofile_path = ofile_path.with_name(f'{ofile_path.name}-{known_st_commit[0:8]}')
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -d {tmpdir} {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_stdout_defaults(self):
        """Test exportpatch to stdout, using default arguments."""
        # run the command, saving output to a file in our tmpdir
        (res, pbody) = my_run_command(f'{test_cmd} {known_st_commit}')
        # ensure command succeeded
        self.assertEqual(res, 0, f'running {test_cmd} failed')
        # create a temp file
        tmpfd, tmpname = tempfile.mkstemp(text=True) 
        # write out our patch to our temp file
        try:
            with os.fdopen(tmpfd, 'w', encoding='utf-8') as tmpf:
                tmpf.write(pbody)
            # compare the commit file with a known good one
            res = filecmp.cmp(tmpname, f'test/data/{known_st_patch}.known_good')
        finally:
            os.remove(tmpname)
        self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_cwd_defaults(self):
        """Test exportpatch to file/dir, using default arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir)
            # make sure our output file doesn't exist (even though its a temp dir)
            ofile_path.unlink(missing_ok=True)
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w {known_st_commit}', cwd=tmpdir)
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_dir_using_reference(self):
        """Test exportpatch to file/dir, passing a a reference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # get name we expect for our patch
            ofile_path = get_patch_path(known_st_patch, dirname=tmpdir)
            # make sure our output file doesn't exist (even though its a temp dir)
            ofile_path.unlink(missing_ok=True)
            # run the command, saving output to a file in our tmpdir
            (res, pname) = my_run_command(f'{test_cmd} -w -d {tmpdir} -F some-reference {known_st_commit}')
            # ensure command succeeded
            self.assertEqual(res, 0, f'running {test_cmd} failed')
            # ensure name returned is the same
            self.assertEqual(pname.strip(), ofile_path.name, 'patch name wrong')
            # compare the commit file with a known good one
            res = filecmp.cmp(ofile_path, f'test/data/{known_st_patch}.some_reference')
            self.assertEqual(res, True, 'patch file differs from known good')


if __name__ == '__main__':
    unittest.main()
