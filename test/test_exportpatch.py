"""The test suite for the patchtools exportpatch command.

Test the local patchtools package 'exportpatch' module,
by calling the code directly.
"""

import filecmp
import tempfile
import unittest
from pathlib import Path

from .util import DATA_PATH, call_mut, compare_text_and_file, get_patch_path, import_mut

# the module under test
MUT = 'exportpatch'

# commit for one file
COMMIT_1F = '8db816c6f176321e42254badd5c1a8df8bfcfdb4'

# commit for multiple files
COMMIT_MF = '362432e9b9aefb914ab7d9f86c9fc384a6620c41'

# a make-believe commit (as of 2026 -- let's hope its always bogus)
COMMIT_BOGUS = '123456789abcde123456789abcde000000000077'

# patch name for known commit (no suffix, etc)
PATCH_1F = 'scsi-st-Tighten-the-page-format-heuristics-with-MODE-SELECT'

# patch name for known commit with multiple files
PATCH_MF = 'scsi-libsas-Add-rollback-handling-when-an-error-occurs'

# patchname for the one file in the simple commit
PATCH_FILE_1F = 'drivers/scsi/st.c'

# patch filename pattern for all files in multiple-file commit
PATCH_FILE_PAT_MF = 'drivers/scsi/libsas/'

# patch filenames for the patch with multiple commits
PATCH_FILES_MF = [
    'drivers/scsi/libsas/sas_init.c',
    'drivers/scsi/libsas/sas_internal.h',
    'drivers/scsi/libsas/sas_phy.c',
    ]

# patchname for one file in mulitple-file commit
PATCH_FILE_FIRST_MF = 'drivers/scsi/libsas/sas_internal.h'

mut = import_mut(MUT)


class TestExportpatchNormalFunctionality(unittest.TestCase):
    """Test normal functionality for 'exportpatch'."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class for this class. Done once per class."""
        cls.assertTrue(DATA_PATH, 'cannot find "data" subdirectory')

    def test_to_file_in_dir_defaults_1f(self):
        """Test exportpatch of one file to file/dir, using defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            (res, pname, err_out) = call_mut(mut, MUT, ['-w', '-d', tmpdir, COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_dir_defaults_mf(self):
        """Test exportpatch of multiple files to file/dir, using defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_MF, dirname=tmpdir)
            (res, pname, err_out) = call_mut(mut, MUT, ['-w', '-d', tmpdir, COMMIT_MF])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_MF}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_in_dir_suffix(self):
        """Test exportpatch to file/dir, with a suffix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir, suffix='.patch')
            (res, pname, err_out) = call_mut(mut, MUT, ['-w', '-d', tmpdir, '-s', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_numeric_default(self):
        """Test exportpatch to file/dir, with numeric filename, using default start."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir, prefix='0001-')
            (res, pname, err_out) = call_mut(mut, MUT, ['-w', '-d', tmpdir, '-n', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_numeric_s2(self):
        """Test exportpatch to file/dir, with numeric filename, using start number 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir, prefix='0002-')
            (res, pname, err_out) = call_mut(mut, MUT, ['-w', '-d', tmpdir, '-n', '-N', '2', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_numeric_w3(self):
        """Test exportpatch to file/dir, with numeric filename, using width of 3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir, prefix='001-')
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-n', '--num-width', '3', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_overwrite_force(self):
        """Test exportpatch to file/dir, where patch already exists, using overwrite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            patch_path_expected.touch()
            (res, pname, err_out) = call_mut(mut, MUT, ['-w', '-d', tmpdir, '-f', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_overwrite_no_force(self):
        """Test exportpatch to file/dir, where patch already exists, not using overwrite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # create an empty 'patch' file, to creat a collision
            patch_name_orig = get_patch_path(PATCH_1F, dirname=tmpdir)
            patch_name_orig.touch()
            # now set up for actual path for patch name expected
            patch_path_expected = \
                    patch_name_orig.with_name(f'{patch_name_orig.name}-{COMMIT_1F[0:8]}')
            (res, pname, err_out) = call_mut(mut, MUT, ['-w', '-d', tmpdir, COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_stdout_defaults(self):
        """Test exportpatch to stdout, using default arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            (res, pbody, err_out) = call_mut(mut, MUT, [COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            res = compare_text_and_file(pbody, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')
            self.assertFalse(patch_path_expected.exists(),
                             'Patch file should not exist')

    def test_to_file_in_cwd_defaults(self):
        """Test exportpatch to file/current-dir, using default arguments."""
        patch_path_expected = get_patch_path(PATCH_1F)
        (res, pname, err_out) = call_mut(mut, MUT, ['-w', COMMIT_1F])
        self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
        self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
        res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.known_good')
        self.assertEqual(res, True, 'patch file differs from known good')
        patch_path_expected.unlink()

    def test_to_file_using_single_reference(self):
        """Test exportpatch to file/dir, passing a single reference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-F', 'some-reference', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.some_reference')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_using_double_reference(self):
        """Test exportpatch to file/dir, passing a double reference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT,
                             ['-w', '-d', tmpdir, '-F', 'some-reference', '-F', 'two more', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{PATCH_1F}.some_reference_twice')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_file_using_signed_off_by(self):
        """Test exportpatch to file/dir, using signed-off-by."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-S', COMMIT_1F])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.signed_off_by')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_to_files_two_commits(self):
        """Test exportpatch to file/dir, with two commits."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected_1 = get_patch_path(PATCH_1F, dirname=tmpdir)
            patch_path_expected_2 = get_patch_path(PATCH_MF, dirname=tmpdir)
            (res, pnames, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, COMMIT_1F, COMMIT_MF])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            pname_arr = pnames.split()
            self.assertEqual(len(pname_arr), 2, f'Needed 2 patchnames returned: {pnames}')
            pname1, pname2 = pname_arr
            self.assertEqual(pname1, patch_path_expected_1.name, 'first patch name wrong')
            self.assertEqual(pname2, patch_path_expected_2.name, 'second patch name wrong')
            res = filecmp.cmp(patch_path_expected_1, f'{DATA_PATH}/{PATCH_1F}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')
            res = filecmp.cmp(patch_path_expected_2, f'{DATA_PATH}/{PATCH_MF}.known_good')
            self.assertEqual(res, True, 'patch file differs from known good')


class TestExportpatchExtract(unittest.TestCase):
    """Test extract functionality for 'exportpatch'."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class for this class. Done once per class."""
        cls.assertTrue(DATA_PATH, 'cannot find "data" subdirectory')

    def test_extract_of_all_1f(self):
        """Test exportpatch that extracts the one file in a patch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-x', PATCH_FILE_1F, COMMIT_1F])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.extracted')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_extract_of_all_mf_pat(self):
        """Test exportpatch that extracts all files in a patch using a pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_MF, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-x', PATCH_FILE_PAT_MF, COMMIT_MF])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_MF}.2f_of_2')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_extract_of_all_mf_multiple_opts(self):
        """Test exportpatch that extracts all files in a patch using multiple options."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_MF, dirname=tmpdir)
            cmd_arr = ['-w', '-d', tmpdir]
            for a_file in PATCH_FILES_MF:
                cmd_arr += ['-x', a_file]
            cmd_arr.append(COMMIT_MF)
            (res, pname, err_out) = call_mut(mut, MUT, cmd_arr)
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_MF}.2f_of_2')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_extract_of_none_1f(self):
        """Test exportpatch that extracts nothing from a patch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (res, _, err_out) = call_mut(mut, MUT,
                    ['-w', '-d', tmpdir, '-x', '/bogus/path', COMMIT_1F])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            # ensure we got an error message saying the patch was skipped
            self.assertTrue('Skipping' in err_out, f'err_out={err_out}')

    def test_extract_of_none_mf(self):
        """Test exportpatch that extracts nothing from a patch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (res, _, err_out) = call_mut(mut, MUT,
                    ['-w', '-d', tmpdir, '-x', '/bogus/path', COMMIT_MF])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            # ensure we got an error message saying the patch was skipped
            self.assertTrue('Skipping' in err_out, f'err_out={err_out}')

    def test_extract_of_one_mf(self):
        """Test exportpatch that extracts one file of two."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_MF, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-x', PATCH_FILES_MF[1], COMMIT_MF])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{PATCH_MF}.extracted_file2_of_3')


class TestExportpatchExclude(unittest.TestCase):
    """Test exclude functionality for 'exportpatch'."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class for this class. Done once per class."""
        cls.assertTrue(DATA_PATH, 'cannot find "data" subdirectory')

    def test_exclude_of_all_1f(self):
        """Test exportpatch that excludes the only file in a single-file patch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (res, _, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-X', PATCH_FILE_1F, COMMIT_1F])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            # ensure we got an error message saying the patch was skipped
            self.assertTrue('Skipping' in err_out, f'err_out={err_out}')

    def test_exlude_of_all_mf_pat(self):
        """Test exportpatch that excludes all files in a patch using a pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (res, _, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-X', PATCH_FILE_PAT_MF, COMMIT_MF])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            # ensure we got an error message saying the patch was skipped
            self.assertTrue('Skipping' in err_out, f'err_out={err_out}')

    def test_exlude_of_all_mf_multiple_opts(self):
        """Test exportpatch that excludes all files with multiple options."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd_arr = ['-w', '-d', tmpdir]
            for a_file in PATCH_FILES_MF:
                cmd_arr += ['-X', a_file]
            cmd_arr.append(COMMIT_MF)
            (res, _, err_out) = call_mut(mut, MUT, cmd_arr)
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            # ensure we got an error message saying the patch was skipped
            self.assertTrue('Skipping' in err_out, f'err_out={err_out}')

    def test_exclude_of_none_1f(self):
        """Test exportpatch exclude of nothing for 1 file patch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_1F, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-X', '/abc/def', COMMIT_1F])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_1F}.extracted')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_exclude_of_none_mf(self):
        """Test exportpatch exclude of nothing for mutliple file patch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_MF, dirname=tmpdir)
            (res, pname, err_out) = \
                    call_mut(mut, MUT, ['-w', '-d', tmpdir, '-X', '/abc/def', COMMIT_MF])
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{PATCH_MF}.extracted')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_exclude_2f_of_multiple(self):
        """Test exportpatch exclude 2 files of multiple files in a patch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(PATCH_MF, dirname=tmpdir)
            cmd_arr = ['-w', '-d', tmpdir]
            cmd_arr += ['-X', PATCH_FILES_MF[0]]
            cmd_arr += ['-X', PATCH_FILES_MF[-1]]
            cmd_arr.append(COMMIT_MF)
            (res, pname, err_out) = call_mut(mut, MUT, cmd_arr)
            self.assertEqual(res, 0, f'running {MUT} failed: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{PATCH_MF}.excluded_first_and_last')
            self.assertEqual(res, True, 'patch file differs from known good')


class TestExportpatchErrorCases(unittest.TestCase):
    """Test error cases for 'exportpatch'."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class for this class. Done once per class."""
        cls.assertTrue(DATA_PATH, 'cannot find "data" subdirectory')

    def test_err_no_commit_supplied(self):
        """Test exportpatch with no commit supplied."""
        (res, _, err_out) = call_mut(mut, MUT, [])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('Must supply' in err_out, f'err_out={err_out}')

    def test_err_invalid_commit_supplied(self):
        """Test exportpatch with no commit supplied."""
        (res, _, err_out) = call_mut(mut, MUT, ['HEAD'])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('must be hashes' in err_out, f'err_out={err_out}')

    def test_err_bogus_commit(self):
        """Test exportpatch with bogus commit."""
        (res, _, err_out) = call_mut(mut, MUT, [COMMIT_BOGUS])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('Skipping' in err_out, f'err_out={err_out}')

    def test_err_bogus_option_short(self):
        """Test exportpatch with bogus argument(s)."""
        (res, _, err_out) = call_mut(mut, MUT, ['-z', COMMIT_BOGUS])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('no such option' in err_out, f'err_out={err_out}')

    def test_err_bogus_args_long(self):
        """Test exportpatch with bogus argument(s)."""
        (res, _, err_out) = call_mut(mut, MUT, ['--zebra', COMMIT_BOGUS])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('no such option' in err_out, f'err_out={err_out}')

    def test_err_num_width_no_commit(self):
        """Test exportpatch with num-width argument with no argument, with no commit."""
        (res, _, err_out) = call_mut(mut, MUT, ['--num-width'])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('requires 1 argument' in err_out, f'err_out={err_out}')

    def test_err_num_width_bogus_commit(self):
        """Test exportpatch with num-width argument with bogus value, with a commit."""
        (res, _, err_out) = call_mut(mut, MUT, ['--num-width', 'XX', COMMIT_BOGUS])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('invalid integer value' in err_out, f'err_out={err_out}')

    def test_err_num_width_valid_commit(self):
        """Test exportpatch with num-width argument with bogus value, with a valid commit."""
        (res, _, err_out) = call_mut(mut, MUT, ['--num-width', 'XX', COMMIT_1F])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('invalid integer value' in err_out, f'err_out={err_out}')

    def test_err_first_number_no_commit(self):
        """Test exportpatch with first-number argument with no argument, with no commit."""
        (res, _, err_out) = call_mut(mut, MUT, ['-N'])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('requires 1 argument' in err_out, f'err_out={err_out}')

    def test_err_first_number_bogus_commit(self):
        """Test exportpatch with first-number argument with bogus value, with a bogus commit."""
        (res, _, err_out) = call_mut(mut, MUT, ['-N', 'XX', COMMIT_BOGUS])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('invalid integer value' in err_out, f'err_out={err_out}')

    def test_err_first_number_valid(self):
        """Test exportpatch with first-number argument with bogus value, with a valid commit."""
        (res, _, err_out) = call_mut(mut, MUT, ['-N', 'XX', COMMIT_1F])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('invalid integer value' in err_out, f'err_out={err_out}')

    def test_err_first_number_out_of_range_too_large(self):
        """Test exportpatch with first-number argument with out of range."""
        (res, _, err_out) = call_mut(mut, MUT, ['-N', '9999', COMMIT_1F])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('needs to be in the range' in err_out, f'err_out={err_out}')

    def test_err_first_number_out_of_range_too_small(self):
        """Test exportpatch with first-number argument with out of range."""
        (res, _, err_out) = call_mut(mut, MUT, ['-N', '-1', COMMIT_BOGUS])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('needs to be in the range' in err_out, f'err_out={err_out}')

    def test_err_reference_with_no_value(self):
        """Test exportpatch with reference with no argument."""
        (res, _, err_out) = call_mut(mut, MUT, ['-F'])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('requires 1 argument' in err_out, f'err_out={err_out}')

    def test_err_export_to_dir_no_value(self):
        """Test exportpatch write to a dir with no argument and no commit."""
        (res, _, err_out) = call_mut(mut, MUT, ['-d'])
        self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('requires 1 argument' in err_out, f'err_out={err_out}')

    def test_err_export_to_dir_no_commit(self):
        """Test exportpatch write to a dir with no commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (res, _, err_out) = call_mut(mut, MUT, ['-d', tmpdir])
            self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('Must supply' in err_out, f'err_out={err_out}')

    def test_err_export_to_dir_does_not_exist(self):
        """Test exportpatch write to a dir that does not exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_dir = Path(tmpdir) / 'some_bogus_dir'
            (res, _, err_out) = call_mut(mut, MUT, ['-w', '-d', fake_dir, COMMIT_1F])
            self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('No such file or directory' in err_out, f'err_out={err_out}')

    def test_err_export_to_dir_readonly(self):
        """Test exportpatch write to a dir that does exist but is readonly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = Path(tmpdir) / 'some_subdir'
            new_dir.mkdir(mode=0o511)
            (res, _, err_out) = call_mut(mut, MUT, ['-w', '-d', new_dir, COMMIT_1F])
            self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('Permission denied' in err_out, f'err_out={err_out}')
