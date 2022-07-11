import redis

from src.database.interfaces import UnitOfWorkInterface


class RedisUnitOfWork(UnitOfWorkInterface):
    def __enter__(self):
        engine: redis.Redis = self.database_client_factory()
        self.database_client: redis.client.Pipeline = engine.pipeline()
        self.database_client.multi()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def commit(self):
        self.database_client.execute()

    def rollback(self):
        self.database_client.reset()

    def __str__(self) -> str:
        return "redis_unit_of_work"

    def __repr__(self) -> str:
        return "RedisUnitOfWork(...)"
