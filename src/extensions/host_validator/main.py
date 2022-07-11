import re
from typing import List

from .exceptions import InvalidHostName, InvalidHosts, InvalidIPAddress

VALID_IP_ADDRESS_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
VALID_HOSTNAME_REGEX = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"


def validate_host(host: str) -> str:

    is_a_valid_ip = re.match(VALID_IP_ADDRESS_REGEX, host)
    is_a_valid_hostname = re.match(VALID_HOSTNAME_REGEX, host)

    if re.match(r"[\d+\W?]+$", host) and not is_a_valid_ip:
        # badIPAddress
        raise InvalidIPAddress

    elif not is_a_valid_hostname:
        # badHostname
        raise InvalidHostName

    return host


def validate_hosts(hosts: List[str]) -> List[str]:
    if "*" in hosts:
        return ["*"]

    error_message = ""
    for host in hosts:
        try:
            validate_host(host)
        except (InvalidIPAddress, InvalidHostName) as error:
            error_message += str(error) + "\n"

    if error_message:
        raise InvalidHosts(error_message)

    return hosts
