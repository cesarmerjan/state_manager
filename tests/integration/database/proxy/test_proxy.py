from src.database import Database
from src.database.facade import DatabaseFacade
from src.database.in_memory.faker import Faker, FakeManager, FakeRepository, FakeUnitOfWork


def test_database():
    database = Database("faker", {})
    assert isinstance(database._facade, DatabaseFacade)

    assert not database.is_connected
    database.connect()
    assert database.is_connected
    database.disconnect()
    assert not database.is_connected


def test_get_database_client():
    database = Database("faker", {})
    database.connect()
    database_client = database.get_client()
    isinstance(database_client, Faker)


def test_client_factory():
    database = Database("faker", {})
    database.connect()
    database_client_1 = database.client_factory()
    isinstance(database_client_1, Faker)
    database_client_2 = database.client_factory()
    isinstance(database_client_2, Faker)


def test_get_manager():
    database = Database("faker", {})
    manager = database.get_manager()
    assert isinstance(manager, FakeManager)


def test_get_unit_of_work():
    database = Database("faker", {})
    database.connect()
    unit_of_work = database.get_unit_of_work()
    assert isinstance(unit_of_work, FakeUnitOfWork)


def test_get_repository():
    database = Database("faker", {})
    Repository = database.get_repository()
    assert Repository == FakeRepository
