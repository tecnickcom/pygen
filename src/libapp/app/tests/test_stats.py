"""Tests for StatsSetup class."""


from unittest import TestCase
from ~#PROJECT#~.stats import StatsSetup


class TestStatsSetup(TestCase):

    def test_init_class(self):
        m = StatsSetup(prefix="test", host='127.0.0.1', port='8125')
        m.stat.incr('test.test')
        self.assertTrue(True)
