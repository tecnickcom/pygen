"""Tests for LoggingSetup class."""

from unittest import TestCase
import pytest
from ~#PROJECT#~.log import LoggingSetup


class TestLoggingSetup(TestCase):

    def test_init_class(self):
        log = LoggingSetup("DEBUG", "tcp", "/dev/log").run()
        log.info("TEST", strfield="value", numfield=1234)
        _, err = self.capfd.readouterr()
        self.assertIn('"message": "TEST"', err)
        self.assertIn('"strfield": "value"', err)
        self.assertIn('"numfield": 1234', err)

    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd
