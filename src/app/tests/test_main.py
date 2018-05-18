"""Tests for ~#PROJECT#~ CLI module."""

import os
from subprocess import PIPE, run
from unittest import TestCase
from ~#PROJECT#~ import __version__ as VERSION
from ~#PROJECT#~ import __release__ as RELEASE
from ~#PROJECT#~ import __program_name__ as PROGRAM
from ~#PROJECT#~.__main__ import __doc__ as DOC
from ~#PROJECT#~.__main__ import cli
from ~#PROJECT#~.__main__ import docopt
from ~#PROJECT#~.constants import Const


FDIR = os.path.dirname(os.path.abspath(__file__))
if 'PREFIX' in os.environ:
    CLICMD = os.path.join(os.environ['PREFIX'], 'bin', PROGRAM)
else:
    CLICMD = '~#PROJECT#~'


class TestMain(TestCase):

    def test_option_help_short(self):
        out = run([CLICMD, '-h'], stdout=PIPE)
        self.assertTrue(b'Usage:' in out.stdout)

    def test_option_help_long(self):
        out = run([CLICMD, '--help'], stdout=PIPE)
        self.assertTrue(b'Usage:' in out.stdout)

    def test_option_version_short(self):
        out = run([CLICMD, '-v'], stdout=PIPE)
        self.assertEqual(out.stdout.strip(), (VERSION + '.' + RELEASE).encode())

    def test_option_version_long(self):
        out = run([CLICMD, '--version'], stdout=PIPE)
        self.assertEqual(out.stdout.strip(), (VERSION + '.' + RELEASE).encode())

    def test_option_log_level_exception(self):
        args = docopt(DOC, ["--log-level=NULL"])
        with self.assertRaises(Exception):
            cli(args, Const())

    def test_option_config_dir_exception(self):
        args = docopt(DOC, ['--config-dir=/wRoNg/pAtH'])
        with self.assertRaises(Exception):
            cli(args, Const())

    def test_cli(self):
        args = docopt(DOC, ["--config-dir=" + os.path.abspath(FDIR + '/../resources/test/etc/~#PROJECT#~')])
        cli(args, Const())
