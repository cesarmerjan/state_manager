import pytest

from src.database.facade import DatabaseComponents
from src.database.facade.exceptions import (InvalidDatabaseDriverType,
                                            InvalidDatabaseManagerType,
                                            InvalidDatabaseRepositoryType,
                                            InvalidDatabaseUnitOfWorkType)
from src.database.in_memory.faker import (FakeManager, FakeRepository,
                                          FakeUnitOfWork)
from src.database.in_memory.redis import (RedisManager, RedisRepository,
                                          RedisUnitOfWork)
from tests.conftest import basic_types


def test_faker_database_components():
    driver = "faker"
    database_components = DatabaseComponents(driver)
    assert database_components.manager == FakeManager
    assert database_components.repository == FakeRepository
    assert database_components.unit_of_work == FakeUnitOfWork


def test_redis_database_components():
    driver = "redis"
    database_components = DatabaseComponents(driver)
    assert database_components.manager == RedisManager
    assert database_components.repository == RedisRepository
    assert database_components.unit_of_work == RedisUnitOfWork


@pytest.mark.parametrize("driver", basic_types)
def test_database_components_driver_exceptions(driver):
    with pytest.raises(InvalidDatabaseDriverType):
        DatabaseComponents(driver)


@pytest.mark.parametrize("manager", basic_types)
def test_database_components_manager_exceptions(manager, monkeypatch):
    def _set_database_components(self, *args, **kwargs):
        self.manager = manager

    driver = "faker"

    monkeypatch.setattr(
        DatabaseComponents, "_set_database_components", _set_database_components
    )

    with pytest.raises(InvalidDatabaseManagerType):
        DatabaseComponents(driver)


@pytest.mark.parametrize("unit_of_work", basic_types)
def test_database_components_unit_of_work_exceptions(unit_of_work, monkeypatch):
    def _set_database_components(self, *args, **kwargs):
        self.unit_of_work = unit_of_work

    driver = "faker"

    monkeypatch.setattr(
        DatabaseComponents, "_set_database_components", _set_database_components
    )

    with pytest.raises(InvalidDatabaseUnitOfWorkType):
        DatabaseComponents(driver)


@pytest.mark.parametrize("repository", basic_types)
def test_database_components_repository_exceptions(repository, monkeypatch):
    def _set_database_components(self, *args, **kwargs):
        self.repository = repository

    driver = "faker"

    monkeypatch.setattr(
        DatabaseComponents, "_set_database_components", _set_database_components
    )

    with pytest.raises(InvalidDatabaseRepositoryType):
        DatabaseComponents(driver)
