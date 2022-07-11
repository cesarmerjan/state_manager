import pytest

from src.extensions.host_validator import validate_host, validate_hosts
from src.extensions.host_validator.exceptions import (InvalidHostName,
                                                      InvalidHosts,
                                                      InvalidIPAddress)


@pytest.mark.parametrize("host", ["localhost", "www.google.com", "192.0.0.1"])
def test_validate_host(host):
    validated_host = validate_host(host)
    assert validated_host == host


@pytest.mark.parametrize(
    "host", ["www.google.com/", "http://www.google.com", "not valid", "localhost:8000"]
)
def test_validate_host_hostname_error(host):
    with pytest.raises(InvalidHostName):
        validate_host(host)


@pytest.mark.parametrize(
    "host",
    [
        "123.355.321.123",
        "256.0.0.0",
        "127-0-0-1",
        "127.0.0.",
        "127.0.0",
        "192.0.0.1.2",
        "127.0.0.1:8000",
    ],
)
def test_validate_host_ip_address_error(host):
    with pytest.raises(InvalidIPAddress):
        validate_host(host)


def test_validate_hosts():
    hosts = ["localhost", "www.google.com", "192.0.0.1"]
    validated_hosts = validate_hosts(hosts)
    assert hosts == validated_hosts


def test_validate_hosts_errors():
    with pytest.raises(InvalidHosts):
        validate_hosts(["right.com", "www.wrong.com/"])

    with pytest.raises(InvalidHosts):
        validate_hosts(["www.google.com/"])
