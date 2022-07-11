from src.database.interfaces import UnitOfWorkInterface

from .main import Faker


class FakeUnitOfWork(UnitOfWorkInterface):
    def __enter__(self):
        self.database_client: Faker = self.database_client_factory()
        self.database_client.start_transaction()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            super().__exit__(exc_type, exc_value, traceback)
        else:
            self.database_client.end_transaction()

    def commit(self):
        return None

    def rollback(self):
        self.database_client.rollback_transaction()

    def __str__(self) -> str:
        return "faker_unit_of_work"

    def __repr__(self) -> str:
        return "FakerUnitOfWork(...)"
