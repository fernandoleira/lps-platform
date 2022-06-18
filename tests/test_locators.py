import pytest


TESTS_POINT_ID = "0faee264-8782-4302-bc9f-2f116c255020"


def test_get_units(client):
    res = client.get("/api/v1/locators")
    assert res.status_code == 200


def test_post_units(client):
    res = client.post("/api/v1/locators", data={
        'title': 'Locator_Point_Test',
        'description': 'This is a testing locator point.',
        'point_type': 'Info',
        'lat': 41.898479,
        'lon': -84.058311,
        'unit_id': '2955e28d-8348-4fb0-9ac6-bc1f23b373a4',
        'point_id': TESTS_POINT_ID
    })
    assert res.status_code == 201
    assert res.json['point_id'] == TESTS_POINT_ID


def test_get_unit(client):
    res = client.get(f"/api/v1/locators/{TESTS_POINT_ID}")
    assert res.status_code == 200
    assert res.json['point_id'] == TESTS_POINT_ID


def test_delete_unit(client):
    res = client.delete(f"/api/v1/locators/{TESTS_POINT_ID}")
    assert res.status_code == 200
