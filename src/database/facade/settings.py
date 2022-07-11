from typing import Optional

from src.extensions.host_validator import validate_host
from src.extensions.host_validator.exceptions import (InvalidHostName,
                                                      InvalidIPAddress)

from .exceptions import InvalidDatabaseType, InvalidHostType, InvalidPortType, InvalidUseSSLType


class DatabaseSettings:

    __slots__ = ("_host", "_port", "_database", "_use_ssl")

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        use_ssl: bool = False
    ) -> "DatabaseSettings":
        self._host = None
        self.host = host
        self._port = None
        self.port = port
        self._database = None
        self.database = database
        self._use_ssl = None
        self.use_ssl = use_ssl

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host: str) -> None:
        if not isinstance(host, (str, type(None))):
            raise InvalidHostType
        if host:
            try:
                validate_host(host)
            except (InvalidHostName, InvalidIPAddress):
                raise InvalidHostType
        self._host = host

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int) -> None:
        if not isinstance(port, (int, type(None))):
            raise InvalidPortType
        self._port = port

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, database: str) -> None:
        if not isinstance(database, (str, type(None))):
            raise InvalidDatabaseType
        self._database = database

    @property
    def use_ssl(self) -> bool:
        return self._use_ssl

    @use_ssl.setter
    def use_ssl(self, use_ssl: bool) -> None:
        if not isinstance(use_ssl, bool):
            raise InvalidUseSSLType
        self._use_ssl = use_ssl

    def to_dict(self):

        settings = {"host": self.host,
                    "port": self.port,
                    "database": self.database,
                    "use_ssl": self.use_ssl}

        return {key: value for key, value in settings.items() if value}

    def __str__(self) -> str:
        return f"Database settings, host:{self.host}, port:{self.port}, database:{self.database}, use_ssl:{self.use_ssl}"

    def __repr__(self) -> str:
        return f"DatabaseSettings(host={self.host}, port={self.port}, database={self.database}, use_ssl={self.use_ssl})"
