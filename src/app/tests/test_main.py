"""Tests for ~#PROJECT#~ CLI module."""

import os
import sys
from subprocess import PIPE, run
from unittest import TestCase
from ~#PROJECT#~ import __version__ as VERSION
from ~#PROJECT#~ import __release__ as RELEASE
from ~#PROJECT#~ import __program_name__ as PROGRAM
from ~#PROJECT#~.__main__ import __doc__ as DOC
from ~#PROJECT#~.__main__ import *
from ~#PROJECT#~.constants import Const


fdir = os.path.dirname(os.path.abspath(__file__))
if 'PREFIX' in os.environ:
    clicmd = os.path.join(os.environ['PREFIX'], 'bin', PROGRAM)
else:
    clicmd = '~#PROJECT#~'


class TestMain(TestCase):

    def test_option_help_short(self):
        cp = run([clicmd, '-h'], stdout=PIPE)
        self.assertTrue(b'Usage:' in cp.stdout)

    def test_option_help_long(self):
        cp = run([clicmd, '--help'], stdout=PIPE)
        self.assertTrue(b'Usage:' in cp.stdout)

    def test_option_version_short(self):
        cp = run([clicmd, '-v'], stdout=PIPE)
        self.assertEqual(cp.stdout.strip(), (VERSION + '.' + RELEASE).encode())

    def test_option_version_long(self):
        cp = run([clicmd, '--version'], stdout=PIPE)
        self.assertEqual(cp.stdout.strip(), (VERSION + '.' + RELEASE).encode())

    def test_option_log_level_exception(self):
        args = docopt(DOC, ["--log-level=NULL"])
        with self.assertRaises(Exception):
            cli(args, Const())

    def test_option_config_dir_exception(self):
        args = docopt(DOC, ['--config-dir=/wRoNg/pAtH'])
        with self.assertRaises(Exception):
            cli(args, Const())

    def test_cli(self):
        args = docopt(DOC, ["--config-dir=" + os.path.abspath(fdir + '/../resources/test/etc/~#PROJECT#~')])
        cli(args, Const())
