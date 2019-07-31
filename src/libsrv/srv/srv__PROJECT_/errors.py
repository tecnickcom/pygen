"""Custom Error Exceptions."""


class InvalidConfigError(Exception):
    """The configuration value is invalid."""

    def __init__(self, message, *args):
        self.message = message
        super(InvalidConfigError, self).__init__(message, *args)

    def __str__(self):
        return "Invalid configuration: {0}".format(self.message)
