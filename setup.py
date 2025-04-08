"""
Setup file for installation
"""

import os
import shutil

from setuptools import Command, setup

class CleanCommand(Command):
    """Clean up after a build"""
    description = 'sort email files based on date in each'
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, f'Must be in package root: {self.cwd}'
        print('removing "./build", and everything under it')
        shutil.rmtree('build', ignore_errors=True)
        print('removing "./scripts", and everything under it')
        shutil.rmtree('scripts', ignore_errors=True)

# create a "scripts" subdirectory and copy our scripts there,
# without the "py" postfix
shutil.rmtree('scripts', ignore_errors=True)
os.makedirs('scripts')
shutil.copyfile('patchtools/exportpatch.py', 'scripts/exportpatch')
shutil.copyfile('patchtools/fixpatch.py', 'scripts/fixpatch')

setup(
    cmdclass = {'clean': CleanCommand},
    author='Jeff Mahoney',
    author_email='jeffm@suse.com',
    name='patchtools',
    packages=['patchtools'],
    scripts=['scripts/exportpatch', 'scripts/fixpatch'],
    version='2.5')

# vim: sw=4 ts=4 et si:
