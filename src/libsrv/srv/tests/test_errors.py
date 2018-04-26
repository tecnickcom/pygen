"""Tests for custom exceptions."""


from unittest import TestCase
from ~#PROJECT#~ import errors as err


class TestErrors(TestCase):

    def test_invalid_config_error(self):
        e = err.InvalidConfigError('TEST')
        self.assertEqual(str(e), "Invalid configuration: TEST")
