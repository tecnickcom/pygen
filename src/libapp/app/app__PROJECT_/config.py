"""Configuration Module."""

import os
import ujson as json
import requests
from . import errors as err


class Config(object):
    """Load Configuration."""

    def __init__(self, const):
        """Initialize default configuration parameters."""
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
            }
        }

    def empty_remote_config(self):
        """Check if the remote configuration settings are empty."""
        return (self.param['remote_config_provider'] == "" or
                self.param['remote_config_endpoint'] == "" or
                self.param['remote_config_path'] == "")

    def get_local_config_params(self, configDir=""):
        """Get the local configuration parameters."""
        if configDir:
            if not os.path.isfile(os.path.join(configDir, self.config_file)):
                raise Exception('Unable to find configuration file in: {0}'.format(configDir))
            self.config_paths.insert(0, configDir)
        for path in self.config_paths:
            cf = os.path.join(path, self.config_file)
            if os.path.isfile(cf):
                with open(cf, 'r') as fp:
                    self.param.update(json.loads(fp.read()))
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
        """Load the remote configuration using the specified provider."""
        method_name = 'get_config_' + str(provider)
        method = getattr(self, method_name)
        return method(endpoint, path, key)

    def get_remote_config_params(self):
        """Load the remote configuration."""
        if self.empty_remote_config():
            return
        return self.get_remote_config(
            self.param['remote_config_provider'],
            self.param['remote_config_endpoint'],
            self.param['remote_config_path'],
            self.param['remote_config_secret_keyring'])

    def get_config_url(self, endpoint, path, key):
        url = "/".join((endpoint.strip('/'), path.strip('/'), self.config_file + '?' + key))
        r = requests.get(url)
        r.raise_for_status()
        self.param.update(r.json())

    def get_config_params(self, configDir="", logLevel=""):
        """Load the configuration data."""
        self.get_local_config_params(configDir)
        self.get_remote_config_params()
        if logLevel:
            self.param['log']['level'] = logLevel

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
