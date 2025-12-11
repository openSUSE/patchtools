# vim: sw=4 ts=4 et si:
#
"""patch class"""

import os
from . import config

__version__ = '2.6'

class PatchException(Exception):
    pass

config = config.Config()
