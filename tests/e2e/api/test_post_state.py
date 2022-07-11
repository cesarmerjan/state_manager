from src import services
from src.schemas.state import StateUuidSchema


def test_post_state(api_client, database, api_header_with_key, session_cookie_name):

    state_data = {
        "payload": {
            "authentication": "LOGGED",
            "permissions": ["add_user", "delete_user"],
        },
        "subject": "1730b54d-5842-4675-a1f9-0d6fe0703557",
        "timeToExpire": {"seconds": 45, "minutes": 15, "hours": 2, "days": 1},
        "audience": {"hosts": ["127.0.0.1"]},
    }

    response = api_client.post("/state/", headers=api_header_with_key, json=state_data)

    assert response.status_code == 201

    session_cookie = None
    for cookie in response.cookies:
        if cookie.name == session_cookie_name:
            session_cookie = cookie

    assert session_cookie

    http_only = False
    for key in session_cookie._rest.keys():
        if key.lower() == "httponly":
            http_only = True

    assert http_only

    assert session_cookie.expires
    assert session_cookie.value

    state_uuid = StateUuidSchema(uuid=session_cookie.value)
    assert state_uuid

    database.connect()

    unit_of_work = database.get_unit_of_work()
    Repository = database.get_repository()

    state = services.get_state(unit_of_work, Repository, state_uuid)

    assert state["payload"] == state_data["payload"]
    assert state["subject"] == state_data["subject"]
    assert state["audience"] == state_data["audience"]["hosts"]
    assert state["issuer"] == "testclient"

    database.disconnect()


def test_post_state_with_defaults(api_client, api_header_with_key):

    state_data = {
        "payload": {
            "authentication": "LOGGED",
            "permissions": ["add_user", "delete_user"],
        },
        "subject": "1730b54d-5842-4675-a1f9-0d6fe0703557",
    }

    response = api_client.post("/state/", headers=api_header_with_key, json=state_data)

    assert response.status_code == 201


def test_post_state_validation_error(api_client, api_header_with_key):

    state_data = {
        "payload": {
            "authentication": "LOGGED",
            "permissions": ["add_user", "delete_user"],
        }
    }

    response = api_client.post("/state/", headers=api_header_with_key, json=state_data)

    assert response.status_code == 422
