from src.database.facade.exceptions import (InvalidDatabaseComponentsType,
                                            InvalidDatabaseDriverType,
                                            InvalidDatabaseManagerType,
                                            InvalidDatabaseRepositoryType,
                                            InvalidDatabaseSettingsType,
                                            InvalidDatabaseType,
                                            InvalidDatabaseUnitOfWorkType,
                                            InvalidHostType, InvalidPortType)


def test_invalid_database_driver_type():
    error = InvalidDatabaseDriverType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_database_manager_type():
    error = InvalidDatabaseManagerType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_unit_of_work_type():
    error = InvalidDatabaseUnitOfWorkType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_database_repository_type():
    error = InvalidDatabaseRepositoryType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_database_settings_type():
    error = InvalidDatabaseSettingsType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_database_component_type():
    error = InvalidDatabaseComponentsType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_host_type():
    error = InvalidHostType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_port_type():
    error = InvalidPortType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_database_type():
    error = InvalidDatabaseType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)
