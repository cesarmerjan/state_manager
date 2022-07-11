from datetime import datetime, timedelta

import pytest

from src.database.in_memory.faker import Faker, FakeRepository, FakeUnitOfWork


def test_fake_repository_set():
    key = "key"
    value = "value"
    repository = FakeRepository(Faker())
    repository.set(key, value)

    faker = Faker()
    assert faker.database[key] == value


def test_fake_repository_get():
    key = "key"
    value = "value"
    faker = Faker()
    faker.database[key] = value
    faker._expirations[key] = datetime.now() + timedelta(seconds=60)

    repository = FakeRepository(Faker())
    result = repository.get(key)

    assert faker.database[key] == result


def test_fake_repository_delete():
    key = "key"
    value = "value"
    faker = Faker()
    faker.database[key] = value

    repository = FakeRepository(Faker())
    repository.delete(key)

    assert not faker.database.get(key)


def test_fake_repository_exists():
    key = "key"
    value = "value"
    faker = Faker()
    faker.database[key] = value
    faker._expirations[key] = datetime.now() + timedelta(seconds=60)

    repository = FakeRepository(Faker())
    assert repository.exists(key)

    assert not repository.exists("wrong")


def test_fake_repository_expiration():
    key = "key"
    value = "value"
    faker = Faker()
    faker.database[key] = value

    repository = FakeRepository(Faker())
    repository.expire(key, timedelta(seconds=0))

    assert faker._expired(key)

    assert not faker.database.get(key)
