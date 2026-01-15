"""The 'test' class for patchtools."""

from .test_exportpatch import TestExportpatchExclude, TestExportpatchExtract, TestExportpatchNormalFunctionality
from .test_fixpatch import TestFixpatchErrorCases, TestFixpatchNormalFunctionality
from .test_patch import TestPatchModuleNormalFunctionality

__all__ = [
    'TestExportpatchExclude',
    'TestExportpatchExtract',
    'TestExportpatchNormalFunctionality',
    'TestFixpatchErrorCases',
    'TestFixpatchNormalFunctionality',
    'TestPatchModuleNormalFunctionality',
    ]

# vim: sw=4 ts=4 et si:
