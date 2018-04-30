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
        self.assertEqual(cfg.config_file, const.CONFIG_FILE_NAME)
        self.assertEqual(cfg.config_paths, const.CONFIG_PATH)
        self.assertEqual(cfg.param["remote_config_provider"], const.REMOTE_CONFIG_PROVIDER)
        self.assertEqual(cfg.param["remote_config_endpoint"], const.REMOTE_CONFIG_ENDPOINT)
        self.assertEqual(cfg.param["remote_config_path"], const.REMOTE_CONFIG_PATH)
        self.assertEqual(cfg.param["remote_config_secret_keyring"], const.REMOTE_CONFIG_SECRET_KEYRING)

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
        os.environ["~#UPROJECT#~_REMOTECONFIGPROVIDER"] = "url"
        os.environ["~#UPROJECT#~_REMOTECONFIGENDPOINT"] = "http://www.example.com"
        os.environ["~#UPROJECT#~_REMOTECONFIGPATH"] = "endpoint/path"
        os.environ["~#UPROJECT#~_REMOTECONFIGSECRETKEYRING"] = "token=0123456789ABCDEF"
        try:
            cfg.get_local_config_params(os.path.abspath(fdir + "/../resources/test/etc/~#PROJECT#~/"))
            self.assertEqual(cfg.param["server"]["port"], 8017)
            self.assertEqual(cfg.param["remote_config_provider"], "url")
            self.assertEqual(cfg.param["remote_config_endpoint"], "http://www.example.com")
            self.assertEqual(cfg.param["remote_config_path"], "endpoint/path")
            self.assertEqual(cfg.param["remote_config_secret_keyring"], "token=0123456789ABCDEF")
        finally:
            os.environ["~#UPROJECT#~_REMOTECONFIGPROVIDER"] = ""
            os.environ["~#UPROJECT#~_REMOTECONFIGENDPOINT"] = ""
            os.environ["~#UPROJECT#~_REMOTECONFIGPATH"] = ""
            os.environ["~#UPROJECT#~_REMOTECONFIGSECRETKEYRING"] = ""

    def test_get_local_config_params(self):
        const = Const()
        cfg = Config(const)
        cfg.get_local_config_params()
        self.assertEqual(cfg.param["server"]["port"], 8016)

    # NOTE: This test requires internet access
    def test_get_config_params_remote(self):
        const = Const()
        const.CONFIG_FILE_NAME = ""
        cfg = Config(const)
        os.environ["~#UPROJECT#~_REMOTECONFIGPROVIDER"] = "url"
        os.environ["~#UPROJECT#~_REMOTECONFIGENDPOINT"] = "https://jsonplaceholder.typicode.com"
        os.environ["~#UPROJECT#~_REMOTECONFIGPATH"] = "posts/97"
        try:
            cfg.get_config_params({"--config-dir": "", "--log-level": "CRITICAL"})
            self.assertEqual(cfg.param["log"]["level"], "CRITICAL")
            self.assertEqual(cfg.param["id"], 97)
        finally:
            os.environ["~#UPROJECT#~_REMOTECONFIGPROVIDER"] = ""
            os.environ["~#UPROJECT#~_REMOTECONFIGENDPOINT"] = ""
            os.environ["~#UPROJECT#~_REMOTECONFIGPATH"] = ""

    def test_get_config_params_local(self):
        const = Const()
        const.CONFIG_FILE_NAME = ""
        cfg = Config(const)
        cfg.get_config_params({"--config-dir": "", "--log-level": ""})
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
        with self.assertRaises(err.InvalidConfigError):
            cfg = Config(const)
            cfg.param['server']['host'] = ""
            cfg.check_config_params()
        with self.assertRaises(err.InvalidConfigError):
            cfg = Config(const)
            cfg.param['server']['port'] = ""
            cfg.check_config_params()
