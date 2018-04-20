"""Tests for Process class."""


from unittest import TestCase
from ~#PROJECT#~.process import Process


class TestProcess(TestCase):

    def test_get_double(self):
        prc = Process(num=123)
        res = prc.get_double()
        self.assertEqual(res["double"], 246)


class TestBenchmarkProcess(object):

    def test_benchmark_get_double(self, benchmark):
        prc = Process(num=123)
        benchmark(prc.get_double)
