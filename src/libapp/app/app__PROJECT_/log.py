"""Logger Module."""

import logging.config
import pythonjsonlogger
import socket
from structlog import configure, processors, stdlib, threadlocal, getLogger


class LoggingSetup(object):
    """Setup a new Logger."""

    def __init__(self, log_level="INFO", log_network='udp', log_address='/dev/log'):
        """Initialize the logger."""
        self.level = {
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'NOTSET': logging.NOTSET
        }
        self.log_level = log_level
        self.syslog_address = log_address
        self.socktype = socket.SOCK_DGRAM
        if log_network == 'tcp':
            self.socktype = socket.SOCK_STREAM
        configure(
            context_class=threadlocal.wrap_dict(dict),
            logger_factory=stdlib.LoggerFactory(),
            wrapper_class=stdlib.BoundLogger,
            processors=[
                stdlib.filter_by_level,
                stdlib.add_logger_name,
                stdlib.add_log_level,
                stdlib.PositionalArgumentsFormatter(),
                processors.TimeStamper(fmt='iso'),
                processors.StackInfoRenderer(),
                processors.format_exc_info,
                processors.UnicodeDecoder(),
                stdlib.render_to_log_kwargs]
        )

    def _get_config_dict(self):
        """Return the logger configuration."""
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'json': {
                    'format': ('%(asctime)s'
                               ' %(created)f'
                               ' %(msecs)d'
                               ' %(relativeCreated)d'
                               ' %(levelname)s'
                               ' %(levelno)s'
                               ' %(name)s'
                               ' %(pathname)s'
                               ' %(filename)s'
                               ' %(module)s'
                               ' %(funcName)s'
                               ' %(lineno)d'
                               ' %(process)d'
                               ' %(processName)s'
                               ' %(thread)d'
                               ' %(threadName)s'
                               ' %(message)s'),
                    'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
                }
            },
            'handlers': {
                'stderr': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'json',
                    'stream': 'ext://sys.stderr'
                },
                'syslog': {
                    'class': 'logging.handlers.SysLogHandler',
                    'address': self.syslog_address,
                    'socktype': self.socktype,
                    'facility': 'local6',
                    'formatter': 'json'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['stderr', 'syslog'],
                    'level': self.level[self.log_level]
                }
            }
        }
        return config

    def run(self):
        """Set and return the Logger object."""
        logging.config.dictConfig(self._get_config_dict())
        return getLogger(__name__)
