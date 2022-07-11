import abc
from typing import Any, Callable

from .exceptions import InvalidDatabaseClientFactoryType


class UnitOfWorkInterface(metaclass=abc.ABCMeta):
    __slots__ = ("_database_client_factory", "database_client")

    def __init__(self, database_client_factory) -> "UnitOfWorkInterface":
        self._database_client_factory = None
        self.database_client_factory = database_client_factory
        self.database_client = None

    @property
    def database_client_factory(self) -> Callable[[], Any]:
        return self._database_client_factory

    @database_client_factory.setter
    def database_client_factory(
        self, database_client_factory: Callable[[], Any]
    ) -> None:
        if not callable(database_client_factory):
            raise InvalidDatabaseClientFactoryType
        self._database_client_factory = database_client_factory

    def __enter__(self) -> "UnitOfWorkInterface":
        self.database_client = self.database_client_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError  # pragma: no cover
