"""Configuration Module."""

import os
import requests
import ujson as json
from . import errors as err


class Config(object):
    """Load Configuration."""

    def __init__(self, const):
        """Initialize default configuration parameters.
        :const: Constant class with default values.
        """
        self.config_file = const.CONFIG_FILE_NAME
        self.config_paths = const.CONFIG_PATH
        self.param = {
            "remote_config_provider": const.REMOTE_CONFIG_PROVIDER,
            "remote_config_endpoint": const.REMOTE_CONFIG_ENDPOINT,
            "remote_config_path": const.REMOTE_CONFIG_PATH,
            "remote_config_secret_keyring": const.REMOTE_CONFIG_SECRET_KEYRING,
            "log": {
                "level": const.LOG_LEVEL,
                "network": const.LOG_NETWORK,
                "address": const.LOG_ADDRESS
            },
            "stats": {
                "prefix": const.STATS_PREFIX,
                "host": const.STATS_HOST,
                "port": const.STATS_PORT
            },
            "server": {
                "host": const.SERVER_HOST,
                "port": const.SERVER_PORT
            }
        }

    def empty_remote_config(self):
        """Check if the remote configuration settings are empty."""
        return (self.param['remote_config_provider'] == "" or
                self.param['remote_config_endpoint'] == "" or
                self.param['remote_config_path'] == "")

    def get_local_config_params(self, config_dir=""):
        """Get the local configuration parameters.
        :config_dir: Local configuration directory (if any).
        """
        if config_dir:
            if not os.path.isfile(os.path.join(config_dir, self.config_file)):
                raise Exception('Unable to find configuration file in: {0}'.format(config_dir))
            self.config_paths.insert(0, config_dir)
        for path in self.config_paths:
            cfgfile = os.path.join(path, self.config_file)
            if os.path.isfile(cfgfile):
                with open(cfgfile, 'r') as fileobj:
                    self.param.update(json.loads(fileobj.read()))
                    break
        # overwrite remote config with environment variables
        self.param['remote_config_provider'] = os.getenv(
            '~#UPROJECT#~_REMOTECONFIGPROVIDER',
            self.param['remote_config_provider'])
        self.param['remote_config_endpoint'] = os.getenv(
            '~#UPROJECT#~_REMOTECONFIGENDPOINT',
            self.param['remote_config_endpoint'])
        self.param['remote_config_path'] = os.getenv(
            '~#UPROJECT#~_REMOTECONFIGPATH',
            self.param['remote_config_path'])
        self.param['remote_config_secret_keyring'] = os.getenv(
            '~#UPROJECT#~_REMOTECONFIGSECRETKEYRING',
            self.param['remote_config_secret_keyring'])

    def get_remote_config(self, provider, endpoint, path, key):
        """Load the remote configuration using the specified provider.
        :provider: Type of remote provide (indentify the method used to retrieve remote config).
        :endpoint: Base URL of the remote configuration system.
        :path:     Path of the configuration directory relative to the endpoint.
        :key:      Secret to add as URL query or another secret key depending on the provider type.
        """
        method_name = 'get_config_' + str(provider)
        method = getattr(self, method_name)
        return method(endpoint, path, key)

    def get_remote_config_params(self):
        """Load the remote configuration."""
        if self.empty_remote_config():
            return None
        return self.get_remote_config(
            self.param['remote_config_provider'],
            self.param['remote_config_endpoint'],
            self.param['remote_config_path'],
            self.param['remote_config_secret_keyring'])

    def get_config_url(self, endpoint, path, key):
        """Load the config from a remote URL.
        :endpoint: Base URL of the remote configuration system.
        :path:     Path of the configuration directory relative to the endpoint.
        :key:      Secret to add as URL query (e.g. token=123456).
        """
        url = "/".join((endpoint.strip('/'), path.strip('/'), self.config_file + '?' + key))
        req = requests.get(url)
        req.raise_for_status()
        self.param.update(req.json())

    def get_config_params(self, opt):
        """Load the configuration data.
        :opt: Dictionary containing the command-line arguments.
        """
        self.get_local_config_params(opt['--config-dir'])
        self.get_remote_config_params()
        if opt['--log-level']:
            self.param['log']['level'] = opt['--log-level']

    def check_config_params(self):
        """Check the validity of configuration parameters."""
        if not self.param['log']['level']:
            raise err.InvalidConfigError('log.level is empty')
        if not self.param['stats']['prefix']:
            raise err.InvalidConfigError('stats.prefix is empty')
        if not self.param['stats']['host']:
            raise err.InvalidConfigError('stats.host is empty')
        if not self.param['stats']['port']:
            raise err.InvalidConfigError('stats.port is empty')
        if not self.param['server']['host']:
            raise err.InvalidConfigError('server.host is empty')
        if not self.param['server']['port']:
            raise err.InvalidConfigError('server.port is empty')
