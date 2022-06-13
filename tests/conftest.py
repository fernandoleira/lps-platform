import os
import pytest
from api import create_app


@pytest.fixture
def app():
    os.environ['FLASK_APP'] = 'api'
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
