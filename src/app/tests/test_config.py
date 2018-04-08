"""Tests for Config class."""

import os
from unittest import TestCase
from ~#PROJECT#~.constants import Const
from ~#PROJECT#~.config import Config
from ~#PROJECT#~ import errors as err

fdir = os.path.dirname(os.path.abspath(__file__))


class TestConfig(TestCase):

    def test_config_init(self):
        const = Const()
        const.CONFIG_FILE_NAME = "test.json"
        const.CONFIG_PATH = "/test/path"
        const.REMOTE_CONFIG_PROVIDER = "url"
        const.REMOTE_CONFIG_ENDPOINT = "http://www.example.com"
        const.REMOTE_CONFIG_PATH = "endpoint"
        const.REMOTE_CONFIG_SECRET_KEYRING = "token=0123456789ABCDEF"
        cfg = Config(const)
        self.assertEqual(cfg.configFile, const.CONFIG_FILE_NAME)
        self.assertEqual(cfg.configPaths, const.CONFIG_PATH)
        self.assertEqual(cfg.param["remoteConfigProvider"], const.REMOTE_CONFIG_PROVIDER)
        self.assertEqual(cfg.param["remoteConfigEndpoint"], const.REMOTE_CONFIG_ENDPOINT)
        self.assertEqual(cfg.param["remoteConfigPath"], const.REMOTE_CONFIG_PATH)
        self.assertEqual(cfg.param["remoteConfigSecretKeyring"], const.REMOTE_CONFIG_SECRET_KEYRING)

    def test_empty_remote_config(self):
        const = Const()
        const.REMOTE_CONFIG_PROVIDER = "E"
        const.REMOTE_CONFIG_ENDPOINT = "E"
        const.REMOTE_CONFIG_PATH = "E"
        cfg = Config(const)
        self.assertFalse(cfg.empty_remote_config())

        const.REMOTE_CONFIG_PROVIDER = ""
        const.REMOTE_CONFIG_ENDPOINT = "E"
        const.REMOTE_CONFIG_PATH = "E"
        cfg = Config(const)
        self.assertTrue(cfg.empty_remote_config())

        const.REMOTE_CONFIG_PROVIDER = "E"
        const.REMOTE_CONFIG_ENDPOINT = ""
        const.REMOTE_CONFIG_PATH = "E"
        cfg = Config(const)
        self.assertTrue(cfg.empty_remote_config())

        const.REMOTE_CONFIG_PROVIDER = "E"
        const.REMOTE_CONFIG_ENDPOINT = "E"
        const.REMOTE_CONFIG_PATH = ""
        cfg = Config(const)
        self.assertTrue(cfg.empty_remote_config())

    def test_get_local_config_params_wrong_dir(self):
        const = Const()
        cfg = Config(const)
        with self.assertRaises(Exception):
            cfg.get_local_config_params("/wRoNg/pAtH")

    def test_get_local_config_params_custom_dir(self):
        const = Const()
        cfg = Config(const)
        os.environ["~#PROJECT#~_REMOTECONFIGPROVIDER"] = "url"
        os.environ["~#PROJECT#~_REMOTECONFIGENDPOINT"] = "http://www.example.com"
        os.environ["~#PROJECT#~_REMOTECONFIGPATH"] = "endpoint/path"
        os.environ["~#PROJECT#~_REMOTECONFIGSECRETKEYRING"] = "token=0123456789ABCDEF"
        try:
            cfg.get_local_config_params(os.path.abspath(fdir + "/../resources/test/etc/~#PROJECT#~/"))
            self.assertEqual(cfg.param["remoteConfigProvider"], "url")
            self.assertEqual(cfg.param["remoteConfigEndpoint"], "http://www.example.com")
            self.assertEqual(cfg.param["remoteConfigPath"], "endpoint/path")
            self.assertEqual(cfg.param["remoteConfigSecretKeyring"], "token=0123456789ABCDEF")
        finally:
            os.environ["~#PROJECT#~_REMOTECONFIGPROVIDER"] = ""
            os.environ["~#PROJECT#~_REMOTECONFIGENDPOINT"] = ""
            os.environ["~#PROJECT#~_REMOTECONFIGPATH"] = ""
            os.environ["~#PROJECT#~_REMOTECONFIGSECRETKEYRING"] = ""

    def test_get_local_config_params(self):
        const = Const()
        cfg = Config(const)
        cfg.get_local_config_params()
        self.assertEqual(cfg.param["log"]["level"], "INFO")

    # NOTE: This test requires internet access
    def test_get_config_params_remote(self):
        const = Const()
        const.CONFIG_FILE_NAME = ""
        cfg = Config(const)
        os.environ["~#PROJECT#~_REMOTECONFIGPROVIDER"] = "url"
        os.environ["~#PROJECT#~_REMOTECONFIGENDPOINT"] = "https://jsonplaceholder.typicode.com"
        os.environ["~#PROJECT#~_REMOTECONFIGPATH"] = "posts/97"
        try:
            cfg.get_config_params(configDir="", logLevel="CRITICAL")
            self.assertEqual(cfg.param["log"]["level"], "CRITICAL")
            self.assertEqual(cfg.param["id"], 97)
        finally:
            os.environ["~#PROJECT#~_REMOTECONFIGPROVIDER"] = ""
            os.environ["~#PROJECT#~_REMOTECONFIGENDPOINT"] = ""
            os.environ["~#PROJECT#~_REMOTECONFIGPATH"] = ""

    def test_get_config_params_local(self):
        const = Const()
        const.CONFIG_FILE_NAME = ""
        cfg = Config(const)
        cfg.get_config_params(configDir="", logLevel="")
        self.assertEqual(cfg.param["log"]["level"], "INFO")

    def test_get_remote_config_unsupported_provider(self):
        const = Const()
        cfg = Config(const)
        with self.assertRaises(AttributeError):
            cfg.get_remote_config("WRONG", "", "", "")

    def test_get_remote_config_wrong_url(self):
        const = Const()
        cfg = Config(const)
        with self.assertRaises(Exception):
            cfg.get_remote_config("url", "http://www.example.com", "wrong/path", "")

    def test_check_config_params(self):
        const = Const()
        with self.assertRaises(err.InvalidConfigError):
            cfg = Config(const)
            cfg.param['log']['level'] = ""
            cfg.check_config_params()
        with self.assertRaises(err.InvalidConfigError):
            cfg = Config(const)
            cfg.param['stats']['prefix'] = ""
            cfg.check_config_params()
        with self.assertRaises(err.InvalidConfigError):
            cfg = Config(const)
            cfg.param['stats']['host'] = ""
            cfg.check_config_params()
        with self.assertRaises(err.InvalidConfigError):
            cfg = Config(const)
            cfg.param['stats']['port'] = ""
            cfg.check_config_params()
