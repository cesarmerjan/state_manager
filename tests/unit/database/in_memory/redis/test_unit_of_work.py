from functools import lru_cache

from fakeredis import FakeStrictRedis


from src.database.in_memory.redis import RedisUnitOfWork


@lru_cache()
def redis_client_factory():
    return FakeStrictRedis(decode_responses=True)


def test_redis_unit_of_work():

    redis_client = redis_client_factory()

    unit_of_work = RedisUnitOfWork(redis_client_factory)

    with unit_of_work:
        assert isinstance(unit_of_work.database_client,
                          type(redis_client.pipeline()))


def test_unit_of_work_commit():
    unit_of_work = RedisUnitOfWork(redis_client_factory)

    key = "key"
    value = "value"

    with unit_of_work:
        unit_of_work.database_client.set(key, value)
        unit_of_work.commit()

    redis_client = redis_client_factory()

    assert redis_client.get(key) == value

    redis_client.delete(key)


def test_unit_of_work_rollback():
    unit_of_work = RedisUnitOfWork(redis_client_factory)

    key = "key"
    value = "value"

    with unit_of_work:
        unit_of_work.database_client.set(key, value)
        unit_of_work.rollback()

    redis_client = redis_client_factory()

    assert redis_client.get(key) == None
