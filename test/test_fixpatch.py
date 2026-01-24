"""The test suite for the patchtools fixpatch command.

Test the local patchtools package 'fixpatch' module,
by calling the code directly.
"""

import filecmp
import shutil
import tempfile
import unittest
from pathlib import Path

from .util import DATA_PATH, call_mut, compare_text_and_file, get_patch_path, import_mut

# the module under test (and the command/script name, as well)
MUT = 'fixpatch'

# simple filename for a patch to be fixed (using 1 file)
FIX_FILE_1F = 'scsi-st-Tighten-the-page-format-heuristics-with-MODE-SELECT'

# some mostly-empty subject testing files, after fixing
SUBJECT_TESTING_FILE = 'subject-testing-file'
SUBJECT_AND_REF_TESTING_FILE = 'subject-and-ref-testing-file'
SUBJECT_AND_SIGNED_OFF_BY = 'subject-and-signed-off-by'

mut = import_mut(MUT)


class TestFixpatchNormalFunctionality(unittest.TestCase):
    """Test normal functionality for 'fixpatch'."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class for this class. Done once per class."""
        cls.assertTrue(DATA_PATH, 'cannot find "data" subdirectory')

    def test_fixpatch_renaming(self):
        """Test fixpatch fix and rename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, [fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{FIX_FILE_1F}.all_fixed')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_no_renaming(self):
        """Test fixpatch without rename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path('temp', dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-r', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{FIX_FILE_1F}.all_fixed')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_add_suffix(self):
        """Test fixpatch rename with a suffix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F,
                                                 dirname=tmpdir,
                                                 suffix='.patch',
                                                 truncate=None)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-s', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected, f'{DATA_PATH}/{FIX_FILE_1F}.all_fixed')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_dry_run(self):
        """Test fixpatch dry run."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_src = f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing'
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(fixpatch_src, fixpatch_dest)
            (res, pbody, err_out) = call_mut(mut, MUT, ['-n', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            res = compare_text_and_file(pbody,
                                        f'{DATA_PATH}/{FIX_FILE_1F}.all_fixed')
            self.assertEqual(res, True, 'patch file differs from known good')
            self.assertFalse(patch_path_expected.exists(),
                             'Patch file should not exist')

    def test_fixpatch_no_force_on(self):
        """Test fixpatch rename with name collision, no force."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            patch_path_expected.touch()
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, _, err_out) = call_mut(mut, MUT, [fixpatch_dest])
            self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('already exists' in err_out,
                            f'err_out={err_out}, expected={patch_path_expected.resolve()}')

    def test_fixpatch_name_only(self):
        """Test fixpatch name-only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-R', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name
                             , 'patch name wrong')
            self.assertFalse(patch_path_expected.exists(),
                             'Patch file should not exist')

    def test_fixpatch_name_only_with_suffix(self):
        """Test fixpatch name-only mode, with suffix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F,
                                                 dirname=tmpdir,
                                                 suffix='.patch',
                                                 truncate=None)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-s', '-R', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.name, 'patch name wrong')
            self.assertFalse(patch_path_expected.exists(), 'Patch file should not exist')

    def test_fixpatch_no_ack(self):
        """Test fixpatch fixing rename, without ack."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-N', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_no_ack')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_no_diffstat_added(self):
        """Test fixpatch rename, without adding diffstat."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing.no_diffstat',
                         fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-D', fixpatch_dest])
            self.assertEqual(res, 0,
                             f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_no_diffstat')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_header_only(self):
        """Test fixpatch rename, without adding diffstat or ack."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing.no_diffstat',
                         fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-H', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_no_ack_or_diffstat')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_update_only(self):
        """Test fixpatch, without adding diffstat, ack, or renaming."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path('temp', dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing.no_diffstat',
                         fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-U', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_no_ack_or_diffstat')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_setting_first_reference(self):
        """Test fixpatch rename, with a new reference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-F', 'fake ref', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_with_single_fake_ref')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_setting_second_reference(self):
        """Test fixpatch rename, with a 2nd reference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing.with_reference',
                         fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-F', 'fake ref', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_with_2nd_ref')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_setting_two_references(self):
        """Test fixpatch rename, with a new reference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing',
                         fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT,
                    ['-F', 'fake ref 1', '-F', 'fake-ref-2', fixpatch_dest])
            self.assertEqual(res, 0,
                             f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_with_double_fake_ref')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_setting_reference_header_only(self):
        """Test fixpatch rename, with a reference, and header-only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing.no_diffstat',
                         fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-H', '-F', 'fake ref', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.fixed_header_only')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_adding_existing_reference(self):
        """Test fixpatch rename, mostly empty patch, testing existing & new references."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path('some-subject-and-ref',
                                                 dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            with Path(fixpatch_dest).open('w', encoding='utf-8') as f:
                print('Subject: some subject and ref', file=f)
                print('References: ref1 ref2', file=f)
            (res, pname, err_out) = call_mut(mut, MUT,
                    ['-F', 'ref3', '-F', 'ref1', fixpatch_dest])
            self.assertEqual(res, 0,
                             f'calling {MUT} returned failure: {res} ({err_out}i')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{SUBJECT_AND_REF_TESTING_FILE}')
            self.assertEqual(res, True, 'patch file differs from expected')

    def test_fixpatch_signed_off_by(self):
        """Test fixpatch rename, with signed-off-by."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT, ['-S', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(),
                             patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.all_fixed.signed_off_by')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_dummy_mainline_single(self):
        """Test fixpatch rename, with a single dummy mainline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut,
                                             MUT, ['-M', 'v9.9.9.9', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.all_fixed.dummy_mainline_single')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_dummy_mainline_dual(self):
        """Test fixpatch rename, with twoo dummy mainlines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path(FIX_FILE_1F, dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            (res, pname, err_out) = call_mut(mut, MUT,
                    ['-M', 'v9.9.9.9', '-M', 'LOL', fixpatch_dest])
            self.assertEqual(res, 0, f'calling {MUT} returned faliure: {err_out}')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.all_fixed.dummy_mainline_double')
            self.assertEqual(res, True, 'patch file differs from known good')

    def test_fixpatch_signed_off_by_alredy_there(self):
        """Test fixpatch rename, mostly empty patch, where signed-off-by already there."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path('some-subject-with-signed-off-by',
                                                 dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            with Path(fixpatch_dest).open('w', encoding='utf-8') as f:
                print('Subject: some subject with signed-off-by', file=f)
                print(file=f)
                print('Signed-off-by: Barney Rubbel <brubbel@suse.com>', file=f)
            (res, pname, err_out) = call_mut(mut, MUT, [fixpatch_dest])
            self.assertEqual(res, 0,
                             f'calling {MUT} returned failure: {res} ({err_out}i')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{SUBJECT_AND_SIGNED_OFF_BY}')
            self.assertEqual(res, True, 'patch file differs from expected')


class TestFixpatchErrorCases(unittest.TestCase):
    """Test error cases for 'fixpatch'."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class for this class. Done once per class."""
        cls.assertTrue(DATA_PATH, 'cannot find "data" subdirectory')

    def test_err_bogus_option_long(self):
        """Test fixpatch with no patch filename supplied."""
        (res, _, err_out) = call_mut(mut, MUT, ['--zzz'])
        self.assertEqual(res, 1,
                         f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('no such option' in err_out, f'err_out={err_out}')

    def test_err_no_patchname_supplied(self):
        """Test fixpatch with no patch filename supplied."""
        (res, _, err_out) = call_mut(mut, MUT, [])
        self.assertEqual(res, 1,
                         f'calling {MUT} expected return of 1, got {res}')
        self.assertTrue('Must supply' in err_out, f'err_out={err_out}')

    def test_err_bogus_filename_supplied(self):
        """Test fixpatch with a bogus patch filename supplied."""
        with tempfile.TemporaryDirectory() as tmpdir:
            non_existant_file_path = Path(tmpdir) / 'bogus'
            (res, _, err_out) = call_mut(mut, MUT,
                                         [non_existant_file_path.as_posix()])
            self.assertEqual(res, 1,
                             f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('No such file or directory' in err_out,
                            f'err_out={err_out}')

    def test_err_no_rename_patch_readonly(self):
        """Test fixpatch no-rename but patch is read only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path('temp', dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            Path(fixpatch_dest).chmod(0o444)
            (res, _, err_out) = call_mut(mut, MUT, ['-r', fixpatch_dest])
            self.assertEqual(res, 1,
                             f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('Permission denied' in err_out,
                            f'err_out={err_out}')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing')
            self.assertEqual(res, True, 'patch file changed when it should not have')

    def test_err_rename_patch_readonly_dir(self):
        """Test fixpatch rename but directory is read only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path('temp', dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            shutil.copy2(f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing', fixpatch_dest)
            Path(tmpdir).chmod(0o555)
            (res, _, err_out) = call_mut(mut, MUT, [fixpatch_dest])
            self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('Permission denied' in err_out, f'err_out={err_out}')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{FIX_FILE_1F}.needs_fixing')
            self.assertEqual(res, True,
                             'patch file changed when it should not have')

    def test_err_empty_patch_no_subject(self):
        """Test fixpatch with an empty file, triggering a no-subject error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fixpatch_dest = f'{tmpdir}/temp'
            Path(fixpatch_dest).touch()
            (res, _, err_out) = call_mut(mut, MUT, [fixpatch_dest])
            self.assertEqual(res, 1, f'calling {MUT} expected return of 1, got {res}')
            self.assertTrue('no Subject line' in err_out,
                            f'err_out={err_out}')

    def test_err_mostly_empty_patch_with_subject_line(self):
        """Test fixpatch with mostly empty file, having only a Subject line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_path_expected = get_patch_path('testing-file', dirname=tmpdir)
            fixpatch_dest = f'{tmpdir}/temp'
            Path(fixpatch_dest).write_text('Subject: testing file', encoding='utf-8')
            (res, pname, err_out) = call_mut(mut, MUT, [fixpatch_dest])
            self.assertEqual(res, 0,
                             f'calling {MUT} returned failure: {res} ({err_out}i')
            self.assertEqual(pname.strip(), patch_path_expected.as_posix(),
                             'patch name wrong')
            res = filecmp.cmp(patch_path_expected,
                              f'{DATA_PATH}/{SUBJECT_TESTING_FILE}')
            self.assertEqual(res, True, 'patch file differs from expected')
