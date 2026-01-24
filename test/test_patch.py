"""The test suite for the patchtools fixpatch command.

Test the local patchtools package 'patch' module,
by calling the exportpatch or fixpatch as needed.
"""

import unittest

from .util import DATA_PATH, call_mut, get_patch_path, import_mut

# the module under test
FIXPATCH = 'fixpatch'
EXPORTPATCH = 'exportpatch'

# simple filename for a patch to be fixed (using 1 file)
FIX_FILE_1F = 'scsi-st-Tighten-the-page-format-heuristics-with-MODE-SELECT'


class TestPatchModuleNormalFunctionality(unittest.TestCase):
    """Test normal functionality for 'fixpatch'."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class for this class. Done once per class."""
        cls.assertTrue(DATA_PATH, 'cannot find "data" subdirectory')
