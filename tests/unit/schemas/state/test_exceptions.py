from src.extensions.host_validator.exceptions import (InvalidHostName,
                                                      InvalidHosts,
                                                      InvalidIPAddress)


def test_invalid_hostname_type():
    error = InvalidHostName()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_hosts_type():
    error = InvalidHosts("message")
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_ip_address_type():
    error = InvalidIPAddress()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)
