from typing import Callable, Optional

from src.database.interfaces import DatabaseManagerInterface

from .main import Faker


class FakeManager(DatabaseManagerInterface):

    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = "0000"
    DEFAULT_DATABASE = "fake"

    def _make_connection_pool(
        self,
        username: Optional[str],
        password: Optional[str],
        timeout: int
    ) -> str:
        return [Faker]

    def _connect(self, username: Optional[str] = None, password: Optional[str] = None, timeout: int = 3) -> None:
        self.connection_pool = self._make_connection_pool(
            username, password, timeout)

    def _get_database_client(self) -> Faker:
        return self.connection_pool[0]()

    def _database_client_factory(self) -> Callable[[], Faker]:
        return self._get_database_client

    @property
    def is_connected(self) -> bool:
        if self.connection_pool:
            return True
        else:
            return False

    def _disconnect(self) -> None:
        if self.connection_pool:
            self.connection_pool = None

    def __str__(self) -> str:
        return f"faker_manager: {self.host}:{self.port}/{self.database}"

    def __repr__(self) -> str:
        return f"FakerManager(host={self.host}, port={self.port}, database={self.database})"
