from src.database.interfaces.exceptions import (
    InvalidDatabaseClientFactoryType,
    DatabaseNotConnected,
    DatabaseConnectionError
)


def test_invalid_database_client_factory_type_exception():
    error = InvalidDatabaseClientFactoryType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_database_not_connected_exception():
    error = DatabaseNotConnected()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_database_connection_error_exception():
    error = DatabaseConnectionError()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)
