import threading
import time

from src.database.in_memory.faker import FakeManager, Faker, FakeUnitOfWork
from src.database.interfaces import UnitOfWorkInterface


def test_fake_unit_of_work_thread_safe():
    def set_to_database(unit_of_work: UnitOfWorkInterface, key: str, value: str):

        with unit_of_work:
            time.sleep(0.001)
            unit_of_work.database_client.set(str(key), str(value))

    faker_manager = FakeManager()
    faker_manager.connect()

    unit_of_work = FakeUnitOfWork(faker_manager.database_client_factory)

    last_value = 2500
    key = "key"

    threads = []
    for i in range(last_value + 1):
        threads.append(
            threading.Thread(target=set_to_database, args=(unit_of_work, key, i))
        )

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    faker = faker_manager.get_database_client()

    assert faker.database[key] == str(last_value)


def test_unit_of_work():
    faker_manager = FakeManager()
    faker_manager.connect()

    unit_of_work = FakeUnitOfWork(faker_manager.database_client_factory)
    with unit_of_work:
        assert isinstance(unit_of_work.database_client, Faker)
