from datetime import timedelta

from src.database.interfaces import RepositoryInterface

from .main import Faker


class FakeRepository(RepositoryInterface):
    database_client: Faker

    def get(self, key: str) -> str:
        return self.database_client.get(key)

    def set(self, key: str, value: str) -> None:
        self.database_client.set(key, value)

    def delete(self, key: str) -> None:
        self.database_client.delete(key)

    def exists(self, key: str) -> bool:
        return self.database_client.exists(key)

    def expire(self, key: str, time: timedelta) -> None:
        self.database_client.expire(key, time)
