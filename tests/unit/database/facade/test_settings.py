import pytest

from src.database.facade import DatabaseSettings
from src.database.facade.exceptions import (InvalidDatabaseType,
                                            InvalidHostType, InvalidPortType)
from tests.conftest import basic_types


def test_database_settings(database_config):
    database_settings = DatabaseSettings(**database_config)

    assert database_settings.host == database_config["host"]
    assert database_settings.port == database_config["port"]
    assert database_settings.database == database_config["database"]

    assert database_settings.to_dict() == database_config

    assert isinstance(database_settings.__str__(), str)
    assert isinstance(database_settings.__repr__(), str)


def test_database_setting_host_exception():
    with pytest.raises(InvalidHostType):
        DatabaseSettings(
            host="0.0.0.0.0",
            port=4,
            database="database"
        )


@pytest.mark.parametrize(
    "host",
    [i for i in basic_types if not isinstance(i, str) and i],
)
def test_database_setting_host_error(host, database_config):

    with pytest.raises(InvalidHostType):
        DatabaseSettings(
            host=host,
            port=database_config["port"],
            database=database_config["database"],
        )


@pytest.mark.parametrize(
    "port",
    [i for i in basic_types if not isinstance(i, int) and i],
)
def test_database_setting_port_error(port, database_config):

    with pytest.raises(InvalidPortType):
        DatabaseSettings(
            host=database_config["host"],
            port=port,
            database=database_config["database"],
        )


@pytest.mark.parametrize(
    "database",
    [i for i in basic_types if not isinstance(i, str) and i],
)
def test_database_setting_database_error(database, database_config):

    with pytest.raises(InvalidDatabaseType):
        DatabaseSettings(
            host=database_config["host"],
            port=database_config["port"],
            database=database,
        )
