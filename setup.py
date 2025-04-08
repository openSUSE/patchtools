"""
Setup file for installation
"""

import os
import shutil

from setuptools import Command, setup

# create a "scripts" subdirectory and copy our scripts there,
# without the "py" postfix
shutil.rmtree("scripts", ignore_errors=True)
os.makedirs("scripts")
shutil.copyfile("patchtools/exportpatch.py", "scripts/exportpatch")
shutil.copyfile("patchtools/fixpatch.py", "scripts/fixpatch")

setup(
    author="Jeff Mahoney",
    author_email="jeffm@suse.com",
    name="patchtools",
    packages=["patchtools"],
    scripts=["scripts/exportpatch", "scripts/fixpatch"],
    version="2.5")

# vim: sw=4 ts=4 et si:
