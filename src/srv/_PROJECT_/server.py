"""JSON Web Sever."""

import os
from . import __version__ as VERSION
from . import __release__ as RELEASE
from . import __program_name__ as PROGRAM
from . import constants as const
from .process import Process
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from http import HTTPStatus
import ujson as json
from datetime import datetime, timezone


class Server(object):
    """JSON Web Server."""

    def __init__(self, cfg, log, stats):
        """Initialize a new Web Server.
        :cfg:   Server configuration dictionary (cfg.param).
        :log:   Logger object.
        :stats: StatsD object.
        """
        self.STATUS_SUCCESS = "success"
        self.STATUS_FAIL = "fail"
        self.STATUS_ERROR = "error"
        self.cfg = cfg
        self.log = log
        self.stats = stats
        self.routes = [
            ('/', 'index', 'List available endpoints.'),
            ('/status', 'status', 'Check this service status.'),
            ('/config', 'config', 'Return the current configuration.'),
            ('/process/<int:num>', 'process', 'Example process.')
        ]
        rules = []
        for path, method, _ in self.routes:
            rules.append(Rule(path, endpoint=method))
        if 'shutdown' in self.cfg['server']:
            rules.append(Rule('/shutdown', endpoint='shutdown'))
        self.url_map = Map(rules)

    def get_status(self, code):
        """Returns a readable http code status (error|fail|success)
        :code: HTTP status code number.
        """
        if code >= 500:
            return self.STATUS_ERROR
        if code >= 400:
            return self.STATUS_FAIL
        return self.STATUS_SUCCESS

    def response_json(self, status, data):
        """Returns a server response in JSON format.
        :status: HTTPStatus code.
        :data:   Data object to include in the response.
        """
        nowtime = datetime.now(timezone.utc)
        request_status = self.get_status(status.value)
        server_url = self.cfg['server']['host'] + ':' + str(self.cfg['server']['port'])
        body = {
            "program": PROGRAM,                # Program name
            "version": VERSION,                # Program version
            "release": RELEASE,                # Program release number
            "url": server_url,                 # Server settings (host, port)
            "datetime": str(nowtime),          # Human-readable date and time when the event occurred
            "timestamp": nowtime.timestamp(),  # Machine-readable UTC timestamp in seconds since EPOCH
            "status": request_status,          # Status code (error|fail|success)
            "code": status.value,              # HTTP status code
            "message": status.description,     # HTTP status message
            "data": data                       # Data payload
        }
        self.stats.incr('http.' + str(status.value))
        if request_status == self.STATUS_SUCCESS:
            self.log.info('HTTP', status=status, data=data)
        else:
            self.log.error('HTTP', status=status, data=data)
        response = Response(json.dumps(body), mimetype='application/json')
        response.status_code = status.value
        return response

    def error_not_found(self, url):
        """Response in case an non-existent path has been requested."""
        return self.response_json(HTTPStatus.NOT_FOUND, {"url": url})

    def on_index(self, request):
        """Returns a list of available entry points."""
        return self.response_json(HTTPStatus.OK, self.routes)

    def on_status(self, request):
        """Returns the status of the service."""
        return self.response_json(HTTPStatus.OK, {"status": "OK"})

    def on_config(self, request):
        """Returns the current configuration."""
        return self.response_json(HTTPStatus.OK, self.cfg)

    def on_process(self, request, num):
        """Example process function."""
        p = Process(num)
        return self.response_json(HTTPStatus.OK, p.get_double())

    def on_shutdown(self, request):
        """Shutdown the server (testing only)."""
        request.environ['werkzeug.server.shutdown']()
        return Response()

    def dispatch_request(self, request):
        """Dispatch the Request to the associated handler."""
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except NotFound:
            return self.error_not_found(request.url)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        """Build a Web Server Gateway Interface"""
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """Dispatch calls to wsgi_app."""
        return self.wsgi_app(environ, start_response)
