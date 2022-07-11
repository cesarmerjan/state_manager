from src.extensions.exception_with_context import ExceptionWithContext


class InvalidPayloadType(ExceptionWithContext):
    """Exception raised for errors in the input value of payload attribute of State class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidPayloadType":
        self.message = f"{self.__class__.__name__}: Invalid payload input value. It must be a dict."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class InvalidSubjectType(ExceptionWithContext):
    """Exception raised for errors in the input value of subject attribute of State class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidPayloadType":
        self.message = f"{self.__class__.__name__}: Invalid subject input value. It must be a string."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class InvalidIssuerType(ExceptionWithContext):
    """Exception raised for errors in the input value of issuer attribute of State class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidPayloadType":
        self.message = f"{self.__class__.__name__}: Invalid issuer input value. It must be a string."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class InvalidTimeToExpireType(ExceptionWithContext):
    """Exception raised for errors in the input value of time_to_expire attribute of State class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidPayloadType":
        self.message = f"{self.__class__.__name__}: Invalid time_to_expire input value. It must be a timedelta."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class InvalidAudienceType(ExceptionWithContext):
    """Exception raised for errors in the input value of audience attribute of State class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidPayloadType":
        self.message = f"{self.__class__.__name__}: Invalid audience input value. It must be a list of strings."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
