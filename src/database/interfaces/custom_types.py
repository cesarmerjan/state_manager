from typing import Any, Callable, Union

# redis.ConnectionPool
# redis.Redis

DatabaseConnectionPool = Any

DatabaseClient = Any

DatabaseClientFactory = Callable[[], DatabaseClient]
