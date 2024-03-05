import json
import os
import schemas
from jsonschema import validate
import requests

SCHEMA_INIT = os.path.abspath(schemas.__file__)
SCHEMA_DIR = os.path.dirname(SCHEMA_INIT)


def test_post_create_user():
    url = 'https://reqres.in/api/users'
    payload = {"name": "morpheus", "job": "leader"}
    response = requests.post(url, data=payload)
    assert response.status_code == 201


def test_post_register_unsuccessful():
    url = 'https://reqres.in/api/register'
    payload = {"email": "sydney@fife"}
    response = requests.post(url, data=payload)
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Missing password"


def test_post_successful_login():
    url = 'https://reqres.in/api/register'
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["token"] == "QpwL5tke4Pnpja7X4"


def test_post_unsuccessful_login_without_payload():
    url = 'https://reqres.in/api/register'
    payload = {}
    response = requests.post(url, data=payload)
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Missing email or username"


def test_get_single_user_not_found():
    url = 'https://reqres.in/api/users/23'
    response = requests.get(url)
    assert response.status_code == 404


def test_delete_user():
    url = 'https://reqres.in/api/users/2'
    response = requests.delete(url)
    assert response.status_code == 204
    body = response.text
    assert body == ''


def test_get_list_user():
    url = 'https://reqres.in/api/users?page=2'
    response = requests.get(url)
    assert response.status_code == 200


def test_put_update_user_info():
    url = 'https://reqres.in/api/users/2'
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.put(url, data=payload)
    assert response.status_code == 200


def test_patch_update_user_info():
    url = 'https://reqres.in/api/users/2'
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.patch(url, data=payload)
    assert response.status_code == 200


def test_list_users_validate_schema():
    response = requests.get('https://reqres.in/api/users?page=2')
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "get_users_list.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_create_user_schema():
    payload = {"name": "morpheus", "job": "leader"}
    response = requests.post('https://reqres.in/api/users', data=payload)
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "post_users.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_get_single_user_info_schema():
    url = 'https://reqres.in/api/users/2'
    response = requests.get(url)
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "get_single_user.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_get_list_unknow_users_schema():
    url = 'https://reqres.in/api/unknown'
    response = requests.get(url)
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "list_unknow.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))
