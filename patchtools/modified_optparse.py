"""Our own 'optparse' class, then does not call sys.exit().

Set up Option Parsing class so that we can
stop the option parser from calling sys.exit()
when it encounters an error."""

from optparse import OptionParser


class OptionParsingError(RuntimeError):
    """An exception raised when parser.error() is called."""
    def __init__(self, msg):
        self.msg = msg


class ModifiedOptionParser(OptionParser):
    """Our own Option Parsing class, that does not call sys.exit()."""
    def error(self, msg):
        raise OptionParsingError(msg)


