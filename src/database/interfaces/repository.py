import abc
from datetime import timedelta

from .custom_types import DatabaseClient


class RepositoryInterface(metaclass=abc.ABCMeta):
    __slots__ = "_database_client"

    def __init__(self, database_client: DatabaseClient) -> "RepositoryInterface":
        self._database_client = None
        self.database_client = database_client

    @property
    def database_client(self) -> DatabaseClient:
        return self._database_client

    @database_client.setter
    def database_client(self, database_client: DatabaseClient) -> None:
        self._database_client = database_client

    @abc.abstractmethod
    def get(self, key: str) -> str:
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def set(self, key: str, value: str) -> None:
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def exists(self, key: str) -> bool:
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def expire(self, key: str, time: timedelta) -> None:
        raise NotImplementedError  # pragma: no cover
