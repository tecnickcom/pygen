"""Tests for StatsSetup class."""


from unittest import TestCase
from ~#PROJECT#~.stats import StatsSetup


class TestStatsSetup(TestCase):

    def test_init_class(self):
        metric = StatsSetup(prefix="test", host='127.0.0.1', port='8125')
        metric.stat.incr('test.test')
        self.assertIsNotNone(metric)
