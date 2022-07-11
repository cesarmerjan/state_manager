import abc
from functools import lru_cache, wraps
from typing import Optional

from .custom_types import (DatabaseClient, DatabaseClientFactory,
                           DatabaseConnectionPool)
from .exceptions import DatabaseConnectionError, DatabaseNotConnected


class DatabaseManagerInterface(metaclass=abc.ABCMeta):

    __slots__ = ("host", "port", "database", "use_ssl", "connection_pool")

    DEFAULT_HOST: str
    DEFAULT_PORT: str
    DEFAULT_DATABASE: str

    def __init__(
        self,
        host: str = None,
        port: str = None,
        database: int = None,
        use_ssl: bool = False
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.use_ssl = use_ssl
        self.connection_pool = None

    def _connection_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.is_connected:
                raise DatabaseNotConnected
            return func(self, *args, **kwargs)

        return wrapper

    @abc.abstractmethod
    def _connect(
        self, username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 3
    ) -> None:
        raise NotImplementedError  # pragma: no cover

    @lru_cache()
    def connect(
        self, username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 3
    ) -> None:
        try:
            return self._connect(username, password, timeout)
        except Exception:
            raise DatabaseConnectionError

    @abc.abstractproperty
    def is_connected(self) -> bool:
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _make_connection_pool(self, *args, **kwargs) -> "DatabaseConnectionPool":
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_database_client(self) -> "DatabaseClient":
        raise NotImplementedError  # pragma: no cover

    @_connection_required
    def get_database_client(self) -> "DatabaseClient":
        return self._get_database_client()

    @abc.abstractmethod
    def _database_client_factory(self) -> "DatabaseClientFactory":
        raise NotImplementedError  # pragma: no cover

    @property
    @_connection_required
    def database_client_factory(self) -> "DatabaseClientFactory":
        return self._database_client_factory()

    @abc.abstractmethod
    def _disconnect(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def disconnect(self) -> None:
        return self._disconnect()
