import pytest
from _pytest.monkeypatch import MonkeyPatch
from fakeredis import FakeStrictRedis

from src.database.in_memory.redis import RedisManager


def get_mocked_redis_manager(
    database_config: dict, monkeypatch: MonkeyPatch
) -> RedisManager:
    def _make_connection_pool(self, *args, **kwargs):
        redis_client = FakeStrictRedis(decode_responses=True)
        return redis_client.connection_pool

    def _get_database_client(self):
        return FakeStrictRedis(connection_pool=self.connection_pool)

    @property
    def is_connected(self) -> bool:
        try:
            connection = self.connection_pool.make_connection()
            connection.connect()
            return True
        except Exception:
            return False

    monkeypatch.setattr(RedisManager, "_make_connection_pool", _make_connection_pool)

    monkeypatch.setattr(RedisManager, "_get_database_client", _get_database_client)

    monkeypatch.setattr(RedisManager, "is_connected", is_connected)

    return RedisManager(**database_config)


def test_manager(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)

    database_manager.connect()

    assert database_manager.host == database_config["host"]
    assert database_manager.port == database_config["port"]
    assert database_manager.database == database_config["database"]

    database_manager._disconnect()


def test_database_manager_get_database_client(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    database_manager.connect()

    database_client_1 = database_manager._get_database_client()
    assert isinstance(database_client_1, FakeStrictRedis)

    database_client_2 = database_manager._get_database_client()
    assert isinstance(database_client_2, FakeStrictRedis)

    database_manager._disconnect()


def test_database_manager_engine_factory(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    database_manager.connect()

    database_client_factory = database_manager.database_client_factory

    database_client_1 = database_client_factory()
    assert isinstance(database_client_1, FakeStrictRedis)

    database_client_2 = database_client_factory()
    assert isinstance(database_client_2, FakeStrictRedis)

    database_manager._disconnect()


def test_instantiation_difference(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    database_manager.connect()

    database_client_1 = database_manager._get_database_client()
    database_client_2 = database_manager._get_database_client()

    assert database_client_1 != database_client_2


def test_class_repr_(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    assert repr(database_manager)


def test_class_str_(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    assert str(database_manager)


def test_connect(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    database_manager.connect()

    assert database_manager.is_connected


def test_disconnect(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    database_manager.connect()

    database_manager._disconnect()

    assert not database_manager.is_connected


def test_disconnect_multiple_times(database_config, monkeypatch):
    database_manager = get_mocked_redis_manager(database_config, monkeypatch)
    database_manager.connect()
    for i in range(5):
        database_manager._disconnect()
