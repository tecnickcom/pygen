"""Example Process class."""


class Process(object):
    """Example process."""

    def __init__(self, num=0):
        """Initialize a new Process.

        :num: Number
        """
        self.num = num

    def get_double(self):
        """Return the number."""
        return {"double": (2 * self.num)}
