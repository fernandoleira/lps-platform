import pytest

def test_app_config(app):
    assert app.config['DEBUG'] == True
    assert app.config['TESTING'] == True

def test_get_home(client):
    assert client.get("/api/v1/").status_code == 200