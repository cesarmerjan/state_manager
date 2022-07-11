from src.extensions.exception_with_context import ExceptionWithContext


class InvalidDatabaseClientFactoryType(ExceptionWithContext):
    """Exception raised for errors in the input value of database_client_factory argument in the UnitOfWork class.
    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseClientFactoryType":
        self.message = f"{self.__class__.__name__}: Invalid database_client_factory input value. It must be a callable."
        super().__init__(self.message)


class DatabaseNotConnected(ExceptionWithContext):
    """Exception raised for errors in methods of the DatabaseManagerInterface class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "DatabaseNotConnected":
        self.message = f"{self.__class__.__name__}: To use this method you need to first connect to the database. You can use 'connect' method for this."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class DatabaseConnectionError(ExceptionWithContext):
    """Exception raised for errors in the connect method of the DatabaseManagerInterface class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "DatabaseNotConnected":
        self.message = f"{self.__class__.__name__}: Database connection not established. Check that the database is available, or that the configs have been entered correctly."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
