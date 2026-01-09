"""Utility functions, common to test_*.py test modules."""

import filecmp
import importlib
import io
import os
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# template for the patch.cfg file we create
PATCH_CFG_TEMPLATE = [
    '[repositories]',
    'search:',
    '  @PATHNAME@',
    '',
    '[contact]',
    'name: Barney Rubbel',
    'email: brubbel@suse.com',
    ]


def get_git_repo_dir():
    """Get a valid Linux git repo path.

    Return results as (success/failure, pathname/error_msg).

    For now, get repo path from environment variable LINUX_GIT.
    """
    linux_git_dir = os.getenv('LINUX_GIT')
    if not linux_git_dir:
        return (False, 'No LINUX_GIT environment variable found')
    if not Path(linux_git_dir).exists():
        return (False, f'LINUX_GIT directory not found: {linux_git_dir}')
    return (True, linux_git_dir)


def create_config_file():
    """Create a minimal config file, for testing.

    Return (success/failure, error_msg/filename).
    """
    (ok, git_repo_reply) = get_git_repo_dir()
    if not ok:
        print(f'Error: {git_repo_reply}')
        return None
    cfp = Path('patch.cfg')
    with cfp.open('w', encoding='utf-8') as configf:
        for aline in PATCH_CFG_TEMPLATE:
            if '@PATHNAME@' in aline:
                print(aline.replace('@PATHNAME@', git_repo_reply), file=configf)
            else:
                print(aline, file=configf)
    return cfp


def import_mut(modname):
    """Import our module under test."""
    try:
        configp = create_config_file()
        dynamic_mod = importlib.import_module(f'patchtools.{modname}')
        main_under_test = dynamic_mod.main
        configp.unlink()
    finally:
        pass
    return main_under_test


def call_mut(mut_func, mut, arg_array):
    """Call the modulue under test, passing in the specified arguments.

    We capture stdout and stderr from the test code and return it.
    """
    save_argv = sys.argv
    sys.argv = [mut, *arg_array]
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    with redirect_stdout(captured_stdout), redirect_stderr(captured_stderr):
        res = mut_func()
    sys.argv = save_argv
    return (res, captured_stdout.getvalue(), captured_stderr.getvalue())


def find_data_dir_path():
    """Find the 'data' directory path, if possible.

    This is the directory where known-good patch files
    are kept.

    Look first in the current directory. If not there,
    then look for a 'test' subdirectory, and look there.
    """
    for data_pathname in ['data', 'test/data', '../data', '../test/data']:
        data_path = Path(data_pathname)
        if data_path.is_dir():
            return data_path
    return None


# set the data directory
DATA_PATH = find_data_dir_path()


def get_patch_path(fname, dirname=None, prefix='', suffix='', truncate=64):
    """Return a patch filename, optionally truncated.

    The truncation code is copied in part from patch.py, so we match it.

    The truncation is used by exportpatch, but not fixpatch.
    """
    if truncate is not None:
        truncate_chars = truncate - len(fname) - len(prefix + suffix)
        if truncate_chars < 0:
            fname = fname[0:truncate_chars]
    fpath = Path(prefix + fname + suffix)
    if dirname:
        fpath = Path(dirname) / fpath
    return fpath


def compare_text_and_file(pbody, fname):
    """Compare supplied patch body with contents of fname."""
    # write out our patch to our temp file into a temporary file
    tmpfd, tmpname = tempfile.mkstemp(text=True)
    try:
        with os.fdopen(tmpfd, 'w', encoding='utf-8') as tmpf:
            tmpf.write(pbody)
        res = filecmp.cmp(tmpname, fname)
    finally:
        os.remove(tmpname)
    return res
