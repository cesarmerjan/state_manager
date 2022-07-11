from src.database.interfaces.custom_types import DatabaseClient, DatabaseClientFactory
from src.database.interfaces import (DatabaseManagerInterface,
                                     RepositoryInterface, UnitOfWorkInterface)

from .facade import DatabaseComponents, DatabaseFacade, DatabaseSettings


class Database:

    __slots__ = ("_facade", )

    def __init__(self, driver: str, config: dict) -> "Database":
        self._facade = DatabaseFacade(
            DatabaseComponents(driver), DatabaseSettings(**config)
        )

    def connect(self, username: str = None, password: str = None, timeout: int = 3) -> None:
        return self._facade.connect(username, password, timeout)

    def disconnect(self) -> None:
        return self._facade.disconnect()

    @property
    def is_connected(self) -> bool:
        return self._facade.is_connected

    def get_client(self) -> DatabaseClient:
        return self._facade.manager.get_database_client()

    @property
    def client_factory(self) -> DatabaseClientFactory:
        return self._facade.manager.database_client_factory

    def get_manager(self) -> DatabaseManagerInterface:
        return self._facade.manager

    def get_unit_of_work(self) -> UnitOfWorkInterface:
        return self._facade.get_unit_of_work()

    def get_repository(self) -> RepositoryInterface:
        return self._facade.get_repository()

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass
