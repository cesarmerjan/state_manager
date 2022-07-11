from src.extensions.exception_with_context import ExceptionWithContext


class InvalidIPAddress(ExceptionWithContext):
    """Exception raised for errors in the input value of host argument in validate_host function.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidIPAddress":
        self.message = f"{self.__class__.__name__}: Invalid host input value. The host is not a valid IP address."
        super().__init__(self.message)


class InvalidHostName(ExceptionWithContext):
    """Exception raised for errors in the input value of host argument in validate_host function.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidHostName":
        self.message = f"{self.__class__.__name__}: Invalid host input value. The host is not a valid hostname based on RFC 1123."
        super().__init__(self.message)


class InvalidHosts(ExceptionWithContext):
    """Exception raised for multiple errors in the input value of host argument in validate_hosts function.

    Args:
        message: compilation of InvalidIPAddress and InvalidHostName messages
    """

    def __init__(self, message: str) -> "InvalidHosts":
        self.message = f"{self.__class__.__name__}: {message}"
        super().__init__(self.message)
