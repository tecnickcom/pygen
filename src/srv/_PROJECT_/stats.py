"""StatsD Client Module."""

import statsd


class StatsSetup(object):
    """Setup a new StatsD client."""

    def __init__(self, prefix="", host='127.0.0.1', port='8125'):
        """Initialize a new StatsD client.

        :prefix: StatsD string prefix that will be used in every bucket name.
        :host: network host address of the StatsD server.
        :port: network port of the StatsD server.
        """
        self.stat = statsd.StatsClient(host=host, port=port, prefix=prefix)
