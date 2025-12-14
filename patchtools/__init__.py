"""
The 'patch' class

Used to represent all patches
"""

from . import config

__version__ = '2.6'

class PatchError(Exception):
    pass

config = config.Config()

__all__ = [
        'command',
        'config',
        'exportpatch',
        'fixpatch',
        'patchops',
        'patch',
        ]

# vim: sw=4 ts=4 et si:
