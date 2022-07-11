import inspect
from typing import Tuple

from src.database.interfaces import (DatabaseManagerInterface,
                                     RepositoryInterface, UnitOfWorkInterface)

from .exceptions import (InvalidDatabaseDriverType, InvalidDatabaseManagerType,
                         InvalidDatabaseRepositoryType,
                         InvalidDatabaseUnitOfWorkType)


class DatabaseComponents:

    __slots__ = ("_driver", "_settings", "_manager", "_unit_of_work", "_repository")

    DRIVERS = ("faker", "redis")

    def __init__(self, driver: str) -> "DatabaseComponents":

        self._driver = None
        self.driver = driver
        self._manager: DatabaseManagerInterface = None
        self._unit_of_work: UnitOfWorkInterface = None
        self._repository: RepositoryInterface = None
        database_components = self._get_database_components()
        self._set_database_components(*database_components)

    @property
    def driver(self) -> str:
        return self._driver

    @driver.setter
    def driver(self, driver: str) -> None:
        if not isinstance(driver, str):
            raise InvalidDatabaseDriverType
        if driver not in self.DRIVERS:
            raise InvalidDatabaseDriverType
        self._driver = driver

    @property
    def manager(self) -> DatabaseManagerInterface:
        return self._manager

    @manager.setter
    def manager(self, manager: DatabaseManagerInterface) -> None:
        if not inspect.isclass(manager):
            raise InvalidDatabaseManagerType
        if not issubclass(manager, DatabaseManagerInterface):
            raise InvalidDatabaseManagerType
        self._manager = manager

    @property
    def unit_of_work(self) -> UnitOfWorkInterface:
        return self._unit_of_work

    @unit_of_work.setter
    def unit_of_work(self, unit_of_work: UnitOfWorkInterface) -> None:
        if not inspect.isclass(unit_of_work):
            raise InvalidDatabaseUnitOfWorkType
        if not issubclass(unit_of_work, UnitOfWorkInterface):
            raise InvalidDatabaseUnitOfWorkType
        self._unit_of_work = unit_of_work

    @property
    def repository(self) -> RepositoryInterface:
        return self._repository

    @repository.setter
    def repository(self, repository: RepositoryInterface) -> None:
        if not inspect.isclass(repository):
            raise InvalidDatabaseRepositoryType
        if not issubclass(repository, RepositoryInterface):
            raise InvalidDatabaseRepositoryType
        self._repository = repository

    def _set_database_components(
        self,
        manager: DatabaseManagerInterface,
        unit_of_work: UnitOfWorkInterface,
        repository: RepositoryInterface,
    ) -> None:
        self.manager = manager
        self.unit_of_work = unit_of_work
        self.repository = repository

    def _get_database_components(
        self,
    ) -> Tuple[DatabaseManagerInterface, UnitOfWorkInterface, RepositoryInterface]:
        if self.driver == "redis":
            from src.database.in_memory.redis import (RedisManager,
                                                      RedisRepository,
                                                      RedisUnitOfWork)

            return (RedisManager, RedisUnitOfWork, RedisRepository)
        if self.driver == "faker":
            from src.database.in_memory.faker import (FakeManager,
                                                      FakeRepository,
                                                      FakeUnitOfWork)

            return (FakeManager, FakeUnitOfWork, FakeRepository)

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass
