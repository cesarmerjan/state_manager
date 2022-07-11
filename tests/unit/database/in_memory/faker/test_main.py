import threading
import time
from datetime import timedelta

import pytest

from src.database.in_memory.faker import Faker
from src.database.in_memory.faker.exceptions import (InvalidKeyOrValueType,
                                                     InvalidKeyType)
from tests.conftest import basic_types


def test_faker_instanciation():
    faker = Faker()

    assert faker
    assert isinstance(faker.database, dict)
    assert isinstance(faker._locker, type(threading.RLock()))


def test_faker_locker():
    def set_to_database(faker: Faker, key: str, value: str):
        faker.start_transaction()
        time.sleep(0.001)
        faker.database[key] = value
        faker.end_transaction()

    faker = Faker()

    last_value = 2500
    key = "key"

    threads = []
    for i in range(last_value + 1):
        threads.append(threading.Thread(
            target=set_to_database, args=(faker, key, i)))

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    assert faker.database[key] == last_value


def test_set_to_database():
    faker = Faker()

    key = "key"
    value = "value"

    faker.set(key, value)

    assert faker.database[key] == value


def test_get_from_database():
    faker = Faker()

    key = "key"
    value = "value"

    faker.database[key] = value

    assert faker.get(key) == value


def test_get_from_database_with_expired():
    faker = Faker()

    key = "key"
    value = "value"

    faker.set(key, value)
    faker.expire(key, timedelta(seconds=0))

    assert not faker.get(key)


def test_delete_from_database():
    faker = Faker()

    key = "key"
    value = "value"

    faker.database[key] = value

    faker.delete(key)

    assert not faker.database.get(key)


def test_exists_in_database():
    faker = Faker()

    key = "key"
    value = "value"

    faker.database[key] = value

    assert faker.exists(key)

    assert not faker.exists("wrong")


def test_expired_exists_in_database():
    faker = Faker()

    key = "key"
    value = "value"

    faker.database[key] = value

    faker.expire(key, timedelta(seconds=0))

    assert not faker.exists(key)


def test_if_faker_is_singleton():
    faker_1 = Faker()

    key = "key"
    value = "value"

    faker_1.database[key] = value

    faker_2 = Faker()

    assert faker_1 == faker_2
    assert faker_1.database == faker_2.database


def test_fake_repository_expiration():
    key = "key"
    value = "value"
    faker = Faker()
    faker.database[key] = value

    faker.expire(key, timedelta(seconds=0))

    assert faker._expired(key)

    assert not faker.database.get(key)


@pytest.mark.parametrize("data", [i for i in basic_types if not isinstance(i, str)])
def test_faker_set_exceptions(data):
    faker = Faker()

    with pytest.raises(InvalidKeyOrValueType):
        faker.set(data, "ok")

    with pytest.raises(InvalidKeyOrValueType):
        faker.set("ok", data)


@pytest.mark.parametrize("key", [i for i in basic_types if not isinstance(i, str)])
def test_faker_get_exceptions(key):
    faker = Faker()

    with pytest.raises(InvalidKeyType):
        faker.get(key)


@pytest.mark.parametrize("key", [i for i in basic_types if not isinstance(i, str)])
def test_faker_delete_exceptions(key):
    faker = Faker()

    with pytest.raises(InvalidKeyType):
        faker.delete(key)


@pytest.mark.parametrize("key", [i for i in basic_types if not isinstance(i, str)])
def test_faker_exists_exceptions(key):
    faker = Faker()

    with pytest.raises(InvalidKeyType):
        faker.exists(key)


@pytest.mark.parametrize("key", [i for i in basic_types if not isinstance(i, str)])
def test_faker_expire_exceptions(key):
    faker = Faker()

    with pytest.raises(InvalidKeyType):
        faker.expire(key, timedelta(seconds=0))
