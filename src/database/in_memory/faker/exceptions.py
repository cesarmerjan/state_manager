from src.extensions.exception_with_context import ExceptionWithContext


class InvalidKeyOrValueType(ExceptionWithContext):
    """Exception raised for errors in the input value of key or value argument in the set method of Faker class.
    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidKeyOrValueType":
        self.message = f"{self.__class__.__name__}: Invalid key or value input value. Both must be string."
        super().__init__(self.message)


class InvalidKeyType(ExceptionWithContext):
    """Exception raised for errors in the input value of key argument in methods of Faker class.
    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidKeyType":
        self.message = (
            f"{self.__class__.__name__}: Invalid key input value. It must be string."
        )
        super().__init__(self.message)
