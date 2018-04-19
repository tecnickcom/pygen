"""Constants."""


class Const(object):
    """Program constants."""

    #: PROGRAM_NAME defines this application name
    PROGRAM_NAME = "~#PROJECT#~"

    #: CONFIG_FILE_NAME is the name of the config file
    CONFIG_FILE_NAME = "config.json"

    #: CONFIG_PATH list the paths where to look for configuration files (in order)
    CONFIG_PATH = [
        "./",
        "config/",
        "~/." + PROGRAM_NAME + "/",
        "/etc/" + PROGRAM_NAME + "/",
    ]

    #: REMOTE_CONFIG_PROVIDER is the remote configuration source type ("url")
    REMOTE_CONFIG_PROVIDER = ""

    #: REMOTE_CONFIG_ENDPOINT is the remote configuration URL (e.g. http://www.example.com)
    REMOTE_CONFIG_ENDPOINT = ""

    #: REMOTE_CONFIG_PATH is the remote configuration path where to search fo the configuration file ("/config/pygen")
    REMOTE_CONFIG_PATH = ""

    #: REMOTE_CONFIG_SECRET_KEYRING secret to add as URL query or another secret key depending on the implementation.
    REMOTE_CONFIG_SECRET_KEYRING = ""

    # --- Log (syslog) ---

    #: LOG_LEVEL defines the default log level: EMERGENCY, ALERT, CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG
    LOG_LEVEL = "INFO"

    #: LOG_NETWORK is the network type used by Syslog (i.e. udp or tcp). Leave emty to disable.
    LOG_NETWORK = "udp"

    #: LOG_ADDRESS is the network address of the Syslog daemon (ip:port) or just (:port). Leave emty to disable.
    LOG_ADDRESS = "/dev/log"

    #: --- StatsD is used to collect usage metrics ---

    #: STATS_PREFIX is the StatsD client's string prefix that will be used in every bucket name.
    STATS_PREFIX = "~#PROJECT#~"

    #: STATS_HOST is the network host address of the StatsD server.
    STATS_HOST = "127.0.0.1"

    #: STATS_PORT is the network port of the StatsD server.
    STATS_PORT = 8125

    # --- Server ---

    #: SERVER_HOST is the network host address of the server.
    SERVER_HOST = "127.0.0.1"

    #: SERVER_PORT is the network port of the server.
    SERVER_PORT = 8016
