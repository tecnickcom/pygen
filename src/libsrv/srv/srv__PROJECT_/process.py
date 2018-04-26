"""Example Process class."""

from lib_~#BASEPROJECT#~.process import Process as LibProcess


class Process(object):
    """Example process."""

    def __init__(self, num=0):
        """Initialize a new Process.
        :num: Number
        """
        self.num = num

    def get_double(self):
        """Return the number."""
        prc = LibProcess(self.num)
        return prc.get_double()
