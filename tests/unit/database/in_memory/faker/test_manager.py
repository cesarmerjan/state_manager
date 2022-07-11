import pytest

from src.database.in_memory.faker import FakeManager, Faker
from src.database.interfaces.exceptions import DatabaseNotConnected


def test_get_database_client():
    fake_manager = FakeManager()

    fake_manager.connect()

    faker_1 = fake_manager._get_database_client()

    faker_2 = fake_manager._get_database_client()

    assert isinstance(faker_1, Faker)
    assert isinstance(faker_2, Faker)
    assert faker_1 == faker_2


def test_database_client_factory():
    fake_manager = FakeManager()

    fake_manager.connect()

    faker_1 = fake_manager._database_client_factory()()

    faker_2 = fake_manager._database_client_factory()()

    assert isinstance(faker_1, Faker)
    assert isinstance(faker_2, Faker)
    assert faker_1 == faker_2


def test_connect():
    fake_manager = FakeManager()

    fake_manager.connect()

    assert fake_manager.is_connected
    assert fake_manager.connection_pool


def test_disconnect():
    fake_manager = FakeManager()

    fake_manager.connect()

    fake_manager._disconnect()

    assert not fake_manager.is_connected
    assert not fake_manager.connection_pool


def test_database_connection_error():

    fake_manager = FakeManager()

    with pytest.raises(DatabaseNotConnected):
        fake_manager.get_database_client()

    with pytest.raises(DatabaseNotConnected):
        fake_manager.database_client_factory
