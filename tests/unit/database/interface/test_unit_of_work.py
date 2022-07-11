import pytest

from src.database.interfaces import UnitOfWorkInterface
from src.database.interfaces.exceptions import InvalidDatabaseClientFactoryType
from tests.conftest import basic_types


@pytest.mark.parametrize(
    "database_client_factory", [i for i in basic_types if not callable(i)]
)
def test_bad_database_client_factory(database_client_factory):

    UnitOfWork = type(
        "UnitOfWork",
        (UnitOfWorkInterface,),
        {"commit": lambda: None, "rollback": lambda: None},
    )

    with pytest.raises(InvalidDatabaseClientFactoryType):
        UnitOfWork(database_client_factory)


def test_unit_of_work_interface():

    UnitOfWork = type(
        "UnitOfWork",
        (UnitOfWorkInterface,),
        {"commit": lambda: None, "rollback": lambda: None},
    )

    unit_of_work = UnitOfWork(lambda: True)

    with unit_of_work:
        assert unit_of_work.database_client
