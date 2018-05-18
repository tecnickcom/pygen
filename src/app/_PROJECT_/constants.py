"""Constants."""


class Const(object):
    """Program constants."""

    #: Application name
    PROGRAM_NAME = "~#PROJECT#~"

    #: Name of the config file
    CONFIG_FILE_NAME = "config.json"

    #: List the paths where to look for configuration files (in order)
    CONFIG_PATH = [
        "./",
        "config/",
        "~/." + PROGRAM_NAME + "/",
        "/etc/" + PROGRAM_NAME + "/",
    ]

    #: Remote configuration source type ("url")
    REMOTE_CONFIG_PROVIDER = ""

    #: Remote configuration URL (e.g. http://www.example.com)
    REMOTE_CONFIG_ENDPOINT = ""

    #: Remote configuration path where to search fo the configuration file ("/config/pygen")
    REMOTE_CONFIG_PATH = ""

    #: Secret to add as URL query or another secret key depending on the implementation
    REMOTE_CONFIG_SECRET_KEYRING = ""

    # --- Log (syslog) ---

    #: Default log level: EMERGENCY, ALERT, CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG
    LOG_LEVEL = "INFO"

    #: Network type used by Syslog (i.e. udp or tcp). Leave emty to disable.
    LOG_NETWORK = "udp"

    #: Network address of the Syslog daemon (ip:port) or just (:port). Leave emty to disable.
    LOG_ADDRESS = "/dev/log"

    #: --- StatsD is used to collect usage metrics ---

    #: StatsD client's string prefix that will be used in every bucket name.
    STATS_PREFIX = "~#PROJECT#~"

    #: Network host address of the StatsD server.
    STATS_HOST = "127.0.0.1"

    #: Network port of the StatsD server.
    STATS_PORT = 8125
