"""Tests for Process class."""


from unittest import TestCase
from ~#PROJECT#~.process import Process


class TestProcess(TestCase):

    def test_get_double(self):
        p = Process(123)
        o = p.get_double()
        self.assertEqual(o["double"], 246)


class TestBenchmarkProcess(object):

    def test_benchmark_get_double(self, benchmark):
        p = Process(123)
        benchmark(p.get_double)
