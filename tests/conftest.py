from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from src.api import create_api
from src.database.facade import (DatabaseComponents, DatabaseFacade,
                                 DatabaseSettings)
from src.database.in_memory.faker import (FakeManager, FakeRepository,
                                          FakeUnitOfWork)

basic_types = [
    1,
    1.2,
    "string",
    [],
    set([]),
    {},
    lambda: "function",
    type("MyClass", (object,), {}),
    True,
    None,
]


@pytest.fixture(scope="function")
def secret_key():
    return "H@ar t0 Gu3ss"


@pytest.fixture(scope="function")
def state_data():
    state_data = {
        "payload": {"user_uuid": "user_uuid"},
        "subject": "user",
        "issuer": "service",
        "time_to_expire": timedelta(seconds=30),
        "audience": ["other_service.com"],
    }
    return state_data


@pytest.fixture(scope="function")
def string_to_sign():
    return "string"


@pytest.fixture(scope="function")
def database_config():
    return {"host": "localhost", "port": 1234, "database": "test"}


@pytest.fixture(scope="function")
def database_manager(database_config):
    return FakeManager(**database_config)


@pytest.fixture(scope="function")
def Repository():
    return FakeRepository


@pytest.fixture(scope="function")
def unit_of_work(database_manager):
    database_manager.connect()
    return FakeUnitOfWork(database_manager.database_client_factory)


@pytest.fixture(scope="function")
def database(database_config):
    components = DatabaseComponents("faker")
    settings = DatabaseSettings(**database_config)
    return DatabaseFacade(components, settings)


@pytest.fixture(scope="function")
def session_cookie_name():
    return "session_id"


@pytest.fixture(scope="function")
def api_key():
    return "H@ar t0 Gu3ss"


@pytest.fixture(scope="function")
def api_header_with_key(api_key):
    return {"Authorization": f"{api_key}"}


@pytest.fixture(scope="function")
def api(api_key, database, session_cookie_name):
    database.connect("", "")
    return create_api(
        api_key=api_key,
        database=database,
        session_cookie_name=session_cookie_name,
    )


@pytest.fixture(scope="function")
def api_client(api):
    with TestClient(api) as api_client:
        yield api_client
