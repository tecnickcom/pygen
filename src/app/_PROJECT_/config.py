"""Configuration Module."""

import os
import ujson as json
import requests
from . import errors as err


class Config(object):
    """Load Configuration."""

    def __init__(self, const):
        """Initialize default configuration parameters."""
        self.configFile = const.CONFIG_FILE_NAME
        self.configPaths = const.CONFIG_PATH
        self.param = {
            "remoteConfigProvider": const.REMOTE_CONFIG_PROVIDER,
            "remoteConfigEndpoint": const.REMOTE_CONFIG_ENDPOINT,
            "remoteConfigPath": const.REMOTE_CONFIG_PATH,
            "remoteConfigSecretKeyring": const.REMOTE_CONFIG_SECRET_KEYRING,
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
        return (self.param['remoteConfigProvider'] == "" or
                self.param['remoteConfigEndpoint'] == "" or
                self.param['remoteConfigPath'] == "")

    def get_local_config_params(self, configDir=""):
        """Get the local configuration parameters."""
        if not not configDir:
            if not os.path.isfile(os.path.join(configDir, self.configFile)):
                raise Exception('Unable to find configuration file in: {0}'.format(configDir))
            self.configPaths.insert(0, configDir)
        for path in self.configPaths:
            cf = os.path.join(path, self.configFile)
            if os.path.isfile(cf):
                with open(cf, 'r') as fp:
                    self.param.update(json.loads(fp.read()))
                    break
        # overwrite remote config with environment variables
        self.param['remoteConfigProvider'] = os.getenv('~#PROJECT#~_REMOTECONFIGPROVIDER', self.param['remoteConfigProvider'])
        self.param['remoteConfigEndpoint'] = os.getenv('~#PROJECT#~_REMOTECONFIGENDPOINT', self.param['remoteConfigEndpoint'])
        self.param['remoteConfigPath'] = os.getenv('~#PROJECT#~_REMOTECONFIGPATH', self.param['remoteConfigPath'])
        self.param['remoteConfigSecretKeyring'] = os.getenv('~#PROJECT#~_REMOTECONFIGSECRETKEYRING', self.param['remoteConfigSecretKeyring'])

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
            self.param['remoteConfigProvider'],
            self.param['remoteConfigEndpoint'],
            self.param['remoteConfigPath'],
            self.param['remoteConfigSecretKeyring'])

    def get_config_url(self, endpoint, path, key):
        url = "/".join((endpoint.strip('/'), path.strip('/'), self.configFile + '?' + key))
        r = requests.get(url)
        r.raise_for_status()
        self.param.update(r.json())

    def get_config_params(self, configDir="", logLevel=""):
        """Load the configuration data."""
        self.get_local_config_params(configDir)
        self.get_remote_config_params()
        if not not logLevel:
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
