"""Setup file for installation.

Not used for Python version >= 3.11

We magically create front-ends for our scripts,
and we cleanup up after ourselves if setup is given
the 'clean' command.
"""

import os
import shutil
from pathlib import Path

from setuptools import Command, setup

# our scripts -- we will create front ends for these
SCRIPT_MODULES = ['exportpatch', 'fixpatch']


class CleanCommand(Command):
    """Clean up after a build"""

    description = 'Clean up after ourselves'
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        if os.getcwd() != self.cwd:
            raise Exception(f'Must be in package root: {self.cwd}')
        print('Removing "build" subdirectory, and everything under it')
        shutil.rmtree('./build', ignore_errors=True)
        print('Removing "scripts" subdirectory, and everything under it')
        shutil.rmtree('./scripts', ignore_errors=True)
        print('Removing egg-info files, if any')
        shutil.rmtree('./patchtools.egg-info', ignore_errors=True)


def create_script_frontend(mod_name):
    """Create a front end for a script module"""
    script_dest = f'scripts/{mod_name}'
    with Path(script_dest).open('w', encoding='utf-8') as d:
        print('#!/usr/bin/python3', file=d)
        print('import re', file=d)
        print('import sys', file=d)
        print(f'from patchtools.{mod_name} import main', file=d)
        print("if __name__ == '__main__':", file=d)
        print('    sys.exit(main())', file=d)
    os.chmod(script_dest, mode=0o755)   # noqa: S103


def setup_scripts():
    """Copy our two top-level scripts into place, and add shebangs"""
    # ensure we have a clean "scripts" subdirectory
    shutil.rmtree('scripts', ignore_errors=True)
    os.makedirs('scripts')
    # create front-ends for our top-level scripts
    for script in SCRIPT_MODULES:
        create_script_frontend(script)


#
# set up our scripts, then run setup() to do the work
#

setup_scripts()

setup(
    cmdclass={'clean': CleanCommand},
    author='Jeff Mahoney',
    author_email='jeffm@suse.com',
    name='patchtools',
    packages=['patchtools'],
    scripts=[f'scripts/{p}' for p in SCRIPT_MODULES],
    version='2.6.1')

# vim: sw=4 ts=4 et si:
