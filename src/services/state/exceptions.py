from src.extensions.exception_with_context import ExceptionWithContext


class InvalidStateDataType(ExceptionWithContext):
    """Exception raised for errors in the input value of state_data argument in create_state function.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidStateDataType":
        self.message = f"{self.__class__.__name__}: Invalid state_data input value. It must be a StateSchema type."
        super().__init__(self.message)


class InvalidUnitOfWorkType(ExceptionWithContext):
    """Exception raised for errors in the input value of unit_of_work argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidUnitOfWorkType":
        self.message = f"{self.__class__.__name__}: Invalid unit_of_work input value. It must be a InMemoryDatabaseUnitOfWork type."
        super().__init__(self.message)


class InvalidStateUuidType(ExceptionWithContext):
    """Exception raised for errors in the input value of state_uuid argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidStateUuidType":
        self.message = f"{self.__class__.__name__}: Invalid state_uuid input value. It must be a StateUuidSchema type."
        super().__init__(self.message)


class InvalidStateType(ExceptionWithContext):
    """Exception raised for errors in the input value of state argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidStateType":
        self.message = f"{self.__class__.__name__}: Invalid state input value. It must be a State type."
        super().__init__(self.message)


class InvalidTimeToExpireType(ExceptionWithContext):
    """Exception raised for errors in the input value of time_to_expire argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidTimeToExpireType":
        self.message = f"{self.__class__.__name__}: Invalid time_to_expire input value. It must be a TimeDeltaSchema type."
        super().__init__(self.message)


class InvalidPayloadType(ExceptionWithContext):
    """Exception raised for errors in the input value of payload argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidPayloadType":
        self.message = f"{self.__class__.__name__}: Invalid payload input value. It must be a dict."
        super().__init__(self.message)


class InvalidIssuerType(ExceptionWithContext):
    """Exception raised for errors in the input value of issuer argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidIssuerType":
        self.message = f"{self.__class__.__name__}: Invalid issuer input value. It must be a IssuerSchema type."
        super().__init__(self.message)


class InvalidSignedStateType(ExceptionWithContext):
    """Exception raised for errors in the input value of signed_state argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidSignedStateType":
        self.message = f"{self.__class__.__name__}: Invalid signed_state input value. It must be a boolean."
        super().__init__(self.message)


class InvalidSignStateType(ExceptionWithContext):
    """Exception raised for errors in the input value of sign_state argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidSignStateType":
        self.message = f"{self.__class__.__name__}: Invalid sign_state input value. It must be a boolean."
        super().__init__(self.message)


class InvalidSecretKeyType(ExceptionWithContext):
    """Exception raised for errors in the input value of secret_key argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidSecretKeyType":
        self.message = f"{self.__class__.__name__}: Invalid secret_key input value. It must be a string."
        super().__init__(self.message)


class InvalidRequesterType(ExceptionWithContext):
    """Exception raised for errors in the input value of requester argument in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidRequesterType":
        self.message = f"{self.__class__.__name__}: Invalid requester input value. It must be a RequesterSchema type."

        super().__init__(self.message)


class StateNotFound(ExceptionWithContext):
    """Exception raised for errors when state is not found in services functions.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "StateNotFound":
        self.message = f"{self.__class__.__name__}: The state does not exist."
        super().__init__(self.message)


class MissingSecretKey(ExceptionWithContext):
    """Exception raised for errors when state is signed and the secret_key was not defined in services function.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "MissingSecretKey":
        self.message = f"{self.__class__.__name__}: To use signed states you need to define a secret_key."
        super().__init__(self.message)


class NotTheAudience(ExceptionWithContext):
    """Exception raised for errors when requester host is not in the state audience.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "NotTheAudience":
        self.message = (
            f"{self.__class__.__name__}: Requester is not the audience for this state."
        )
        super().__init__(self.message)
