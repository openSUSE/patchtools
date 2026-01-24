"""Setup file for installation.

Not used for Python version >= 3.11

We magically create front-ends for our scripts,
and we cleanup up after ourselves if setup is given
the 'clean' command.
"""

import os
import shutil

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
        print('Removing egg-info files, if any')
        shutil.rmtree('./patchtools.egg-info', ignore_errors=True)


setup(
    cmdclass={'clean': CleanCommand},
    author='Jeff Mahoney',
    author_email='jeffm@suse.com',
    name='patchtools',
    packages=['patchtools'],
    entry_points={
        'console_scripts': [f'{m} = patchtools.{m}:main' for m in SCRIPT_MODULES],
        },
    version='2.5')

# vim: sw=4 ts=4 et si:
