"""Example Class."""


class Example(object):
    """Setup a new Example."""

    def __init__(self, num=0):
        """Initialize a new Example.
        :num: Input number.
        """
        self.num = num

    def get_double(self):
        return 2 * self.num
