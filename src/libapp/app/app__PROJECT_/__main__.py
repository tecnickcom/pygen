"""
~#PROJECT#~

Usage:
  ~#PROJECT#~ [--config-dir=<config-dir>] [--log-level=<log-level>]
  ~#PROJECT#~ -h | --help
  ~#PROJECT#~ -v | --version

Options:
  -c --config-dir=<config-dir>  Configuration directory to be added on top of the search list
  -l --log-level=<log-level>    Log level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
  -h --help                     Show this screen.
  -v --version                  Show version.

Examples:
  ~#PROJECT#~ -c /home/user/config

Note:
  ~#SHORTDESCRIPTION#~
"""


import sys
from docopt import docopt
from . import __version__ as VERSION
from . import __release__ as RELEASE
from .constants import Const
from .config import Config
from .log import LoggingSetup
from .stats import StatsSetup
from .process import Process


def cli(options, const):
    """Main process.
    :options: Command-line arguments as parsed by docopt
    :const:   Constants
    """
    try:
        # initialize unconfigured log
        log = LoggingSetup().run()

        # load configuration
        cfg = Config(const)
        cfg.get_config_params(options)
        cfg.check_config_params()

        # setup logger
        log = LoggingSetup(
            log_level=cfg.param['log']['level'],
            log_network=cfg.param['log']['network'],
            log_address=cfg.param['log']['address']).run()

        # setup statsd to collect metrics
        metric = StatsSetup(
            prefix=cfg.param['stats']['prefix'],
            host=cfg.param['stats']['host'],
            port=cfg.param['stats']['port'])

        # log program start
        metric.stat.incr('start')
        log.info(
            "START",
            version=VERSION,
            release=RELEASE,
            arguments=options,
            config=cfg.param)

        # main process
        proc = Process(123)
        return proc.get_double()

    except BaseException as err:
        log.exception(err)
        raise


def main():
    """Main CLI entrypoint."""
    cli(docopt(__doc__, version=VERSION + '.' + RELEASE), Const())  # pragma: no cover


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
