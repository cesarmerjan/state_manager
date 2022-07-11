import pytest

from src import services
from src.schemas.state import IssuerSchema, StateSchema, StateUuidSchema
from src.services.state.exceptions import StateNotFound


def test_delete_state_without_session_cookie(api_client, api_header_with_key):

    response = api_client.delete("/state/", headers=api_header_with_key)

    assert response.status_code == 400


def test_delete_state(api_client, api_header_with_key, database, session_cookie_name):
    database.connect()

    unit_of_work = database.get_unit_of_work()
    Repository = database.get_repository()

    state_data = StateSchema(
        payload={
            "authentication": "LOGGED",
            "permissions": ["add_user", "delete_user"],
        },
        subject="1730b54d-5842-4675-a1f9-0d6fe0703557",
    )

    issuer = IssuerSchema(host="testclient")

    state = services.create_state(state_data, issuer)

    services.set_state(unit_of_work, Repository, state)

    response = api_client.delete(
        "/state/",
        headers=api_header_with_key,
        cookies={session_cookie_name: state.uuid},
    )

    assert response.status_code == 202

    assert not response.cookies.get(session_cookie_name)

    with pytest.raises(StateNotFound):
        services.get_state(unit_of_work, Repository, StateUuidSchema(uuid=state.uuid))

    database.disconnect()


def test_delete_state_not_the_audience_error(
    api_client, api_header_with_key, database, session_cookie_name
):
    state_data = StateSchema(
        payload={
            "authentication": "LOGGED",
            "permissions": ["add_user", "delete_user"],
        },
        subject="1730b54d-5842-4675-a1f9-0d6fe0703557",
        audience={"hosts": ["127.0.0.1"]},
    )

    issuer = IssuerSchema(host="testclient")
    state = services.create_state(state_data, issuer)

    database.connect()
    unit_of_work = database.get_unit_of_work()
    Repository = database.get_repository()
    services.set_state(unit_of_work, Repository, state)

    response = api_client.delete(
        "/state/",
        headers=api_header_with_key,
        cookies={session_cookie_name: state.uuid},
    )

    assert response.status_code == 403

    database.disconnect()
