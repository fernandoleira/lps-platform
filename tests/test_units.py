import pytest


TESTS_UNIT_ID = "4fc3be87-2db4-415e-bc24-9b5b1731d2a7"


def test_get_units(client):
    res = client.get("/api/v1/units")
    assert res.status_code == 200


def test_post_units(client):
    res = client.post("/api/v1/units", data={
        'name': 'test_unit',
        'user_id': '46dcda39-d7f8-4208-9e46-c97c8bba27d9',
        'alert_mail': 'false',
        'alert_sms': 'false',
        'unit_id': TESTS_UNIT_ID
    })
    assert res.status_code == 201
    assert res.json['unit_id'] == TESTS_UNIT_ID


def test_get_unit(client):
    res = client.get(f"/api/v1/units/{TESTS_UNIT_ID}")
    assert res.status_code == 200
    assert res.json['unit_id'] == TESTS_UNIT_ID


def test_delete_unit(client):
    res = client.delete(f"/api/v1/units/{TESTS_UNIT_ID}")
    assert res.status_code == 200
