"""The test suite for the patchtools fixpatch command.

Test the local patchtools package 'patch' module,
by calling the exportpatch or fixpatch as needed.
"""

import unittest

from patchtools.patch import Patch
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

    def test_remove_mime_headers(self):
        """Test remove_mime_headers removes MIME headers from a patch."""
        patch_text = (
            "From: Author <author@example.com>\n"
            "Date: Tue, 11 Mar 2025 13:25:16 +0200\n"
            "Subject: Test patch\n"
            "MIME-Version: 1.0\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: 8bit\n"
            "\n"
            "Patch body\n"
        )
        p = Patch()
        p.from_email(patch_text)
        self.assertIn('MIME-Version', p.message)
        self.assertIn('Content-Type', p.message)
        self.assertIn('Content-Transfer-Encoding', p.message)
        p.remove_mime_headers()
        self.assertNotIn('MIME-Version', p.message)
        self.assertNotIn('Content-Type', p.message)
        self.assertNotIn('Content-Transfer-Encoding', p.message)

