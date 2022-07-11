import pytest

from src.database.facade import (DatabaseComponents, DatabaseFacade,
                                 DatabaseSettings)
from src.database.facade.exceptions import (InvalidDatabaseComponentsType,
                                            InvalidDatabaseSettingsType)
from src.database.in_memory.faker import (FakeManager, FakeRepository,
                                          FakeUnitOfWork)
from src.database.in_memory.redis import (RedisManager, RedisRepository,
                                          RedisUnitOfWork)
from tests.conftest import basic_types


def test_faker_instanciation():
    database = DatabaseFacade(DatabaseComponents("faker"), DatabaseSettings())

    assert isinstance(database.manager, FakeManager)

    assert database.manager == database.manager

    database.connect()

    assert database.get_repository() == FakeRepository
    assert isinstance(database.get_unit_of_work(), FakeUnitOfWork)


def test_redis_instanciation():
    database = DatabaseFacade(DatabaseComponents("redis"), DatabaseSettings())

    assert isinstance(database.manager, RedisManager)

    assert database.manager == database.manager

    database.connect()

    assert database.get_repository() == RedisRepository
    assert isinstance(database.get_unit_of_work(), RedisUnitOfWork)


def test_facade_connection():
    database = DatabaseFacade(DatabaseComponents("faker"), DatabaseSettings())

    assert not database.is_connected
    database.connect()
    assert database.is_connected
    database.disconnect()
    assert not database.is_connected


@pytest.mark.parametrize("components", basic_types)
def test_database_facade_components_exceptions(components):
    with pytest.raises(InvalidDatabaseComponentsType):
        DatabaseFacade(components, DatabaseSettings())


@pytest.mark.parametrize("settings", basic_types)
def test_database_facade_settings_exceptions(settings):
    with pytest.raises(InvalidDatabaseSettingsType):
        DatabaseFacade(DatabaseComponents("faker"), settings)
