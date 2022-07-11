import uuid
from datetime import timedelta
from time import sleep

from fakeredis import FakeStrictRedis

from src.database.in_memory.redis import RedisRepository


def test_repository_get():

    key = str(uuid.uuid4())
    value = "state"
    redis = FakeStrictRedis()
    pipeline = redis.pipeline()
    redis.set(key, value)

    repository = RedisRepository(pipeline)

    state: bytes = repository.get(key)

    assert state.decode() == value


def test_repository_delete():
    key = str(uuid.uuid4())
    value = "state"
    redis = FakeStrictRedis()
    pipeline = redis.pipeline()
    redis.set(key, value)

    repository = RedisRepository(pipeline)

    state: bytes = repository.delete(key)

    assert not state


def test_repository_set():
    key = str(uuid.uuid4())
    value = "state"
    redis = FakeStrictRedis()
    pipeline = redis.pipeline()
    repository = RedisRepository(pipeline)
    repository.set(key, value)
    pipeline.execute()

    state: bytes = redis.get(key)

    assert state.decode() == value


def test_repository_exists():
    key = str(uuid.uuid4())
    value = "state"
    redis = FakeStrictRedis()
    redis.set(key, value)

    pipeline = redis.pipeline()
    repository = RedisRepository(pipeline)
    assert repository.exists(key)

    assert not repository.exists(str(uuid.uuid4()))


def test_repository_expire():
    key = str(uuid.uuid4())
    value = "state"
    redis = FakeStrictRedis()
    redis.set(key, value)

    pipeline = redis.pipeline()
    repository = RedisRepository(pipeline)

    repository.expire(key, timedelta(seconds=0))
    pipeline.execute()
    assert not redis.get(key)
