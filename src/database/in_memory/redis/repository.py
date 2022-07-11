from datetime import timedelta

from redis.client import Pipeline

from src.database.interfaces import RepositoryInterface


class RedisRepository(RepositoryInterface):
    database_client: Pipeline

    def get(self, key: str) -> str:
        return self.database_client.immediate_execute_command("GET", key)

    def set(self, key: str, value: str) -> None:
        self.database_client.set(key, value)

    def delete(self, key: str) -> None:
        self.database_client.delete(key)

    def exists(self, key: str) -> bool:
        return self.database_client.immediate_execute_command("exists", key)

    def expire(self, key: str, time: timedelta) -> None:
        self.database_client.expire(key, time)
