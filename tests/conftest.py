import pytest
from werkzeug.serving import make_server
from threading import Thread
from tests.test_webapp.app import app


class ServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server("127.0.0.1", 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


@pytest.fixture(scope="session")
def server():
    server = ServerThread(app)
    server.start()
    yield server
    server.shutdown()
