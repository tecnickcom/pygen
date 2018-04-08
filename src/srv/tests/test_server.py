"""Tests for Server module."""


from unittest import TestCase
from ~#PROJECT#~.server import Server
from werkzeug.wrappers import Request
from werkzeug.test import create_environ


class TestServer(TestCase):

    def test_get_status(self):
        srv = Server({"server": {"host": "127.0.0.1", "port": 8765}}, None, None)
        self.assertEqual(srv.get_status(500), srv.STATUS_ERROR)
        self.assertEqual(srv.get_status(404), srv.STATUS_FAIL)
        self.assertEqual(srv.get_status(200), srv.STATUS_SUCCESS)

    def test_dispatch_request_exception(self):
        srv = Server({"server": {"host": "127.0.0.1", "port": 8765}}, None, None)
        environ = create_environ('', '')
        srv.dispatch_request(Request(environ))
