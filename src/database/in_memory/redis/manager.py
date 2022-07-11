from typing import Callable, Optional

import redis

from src.database.interfaces import DatabaseManagerInterface


class RedisManager(DatabaseManagerInterface):

    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = "6379"
    DEFAULT_DATABASE = 0

    def _make_connection_pool(
        self, username: Optional[str],
        password: Optional[str],
        timeout: int
    ) -> redis.ConnectionPool:
        config = {
            "host": self.host or self.DEFAULT_HOST,
            "port": self.port or self.DEFAULT_PORT,
            "db": self.database or self.DEFAULT_DATABASE,
            "username": username,
            "password": password,
        }

        config = {key: value for key, value in config.items() if value}

        connection_pool_kwargs = {
            **config,
            "decode_responses": True,
            "socket_timeout": timeout
        }

        if self.use_ssl:
            connection_pool_kwargs["connection_class"] = redis.connection.SSLConnection
            connection_pool_kwargs["ssl_cert_reqs"] = None

        return redis.ConnectionPool(**connection_pool_kwargs)

    def _connect(
            self,
            username: Optional[str] = None,
            password: Optional[str] = None,
            timeout: int = 3
    ) -> None:

        self.connection_pool = self._make_connection_pool(
            username, password, timeout)

    def _get_database_client(self) -> redis.Redis:

        database_client_kwargs = {
            "connection_pool": self.connection_pool
        }
        if self.use_ssl:
            database_client_kwargs["ssl"] = True

        return redis.Redis(**database_client_kwargs)

    def _database_client_factory(self) -> Callable[[], redis.Redis]:
        return self._get_database_client

    @property
    def is_connected(self) -> bool:
        try:
            connection = self.connection_pool.make_connection()
            connection.connect()
            return True
        except (
            redis.ConnectionError,
            ConnectionRefusedError,
            redis.RedisError,
            redis.TimeoutError
        ):
            return False

    def _disconnect(self) -> None:
        if self.connection_pool:
            self.connection_pool.disconnect()
        self.connection_pool = None

    def __str__(self) -> str:
        return f"redis_manager: {self.host}:{self.port}/{self.database}"

    def __repr__(self) -> str:
        return f"RedisManager(host={self.host}, port={self.port}, database={self.database})"
