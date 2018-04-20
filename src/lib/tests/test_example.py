"""Tests for StatsSetup class."""


from unittest import TestCase
from ~#PROJECT#~.example import Example


class TestExample(TestCase):

    def test_init_class(self):
        ex = Example(num=123)
        self.assertEqual(ex.get_double(), 246)


class TestBenchmarkProcess(object):

    def test_benchmark_get_double(self, benchmark):
        ex = Example(num=123)
        benchmark(ex.get_double)
