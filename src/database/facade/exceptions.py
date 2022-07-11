from src.extensions.exception_with_context import ExceptionWithContext


class InvalidDatabaseDriverType(ExceptionWithContext):
    """Exception raised for errors in the input value of driver attribute in the DatabaseComponents class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseDriverType":
        self.message = f"{self.__class__.__name__}: Invalid driver input value. It must be a valid database driver."
        super().__init__(self.message)


class InvalidDatabaseManagerType(ExceptionWithContext):
    """Exception raised for errors when the value of _manager attribute is set with the _set_database_components method in the DatabaseComponents class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseManagerType":
        self.message = f"{self.__class__.__name__}: Invalid _manager input value. It must be a subclass of DatabaseManagerInterface."
        super().__init__(self.message)


class InvalidDatabaseUnitOfWorkType(ExceptionWithContext):
    """Exception raised for errors when the value of _unit_of_work attribute is set with the _set_database_components method in the DatabaseComponents class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseUnitOfWorkType":
        self.message = f"{self.__class__.__name__}: Invalid _unit_of_work input value. It must be a subclass of UnitOfWorkInterface."
        super().__init__(self.message)


class InvalidDatabaseRepositoryType(ExceptionWithContext):
    """Exception raised for errors when the value of _repository attribute is set with the _set_database_components method in the DatabaseComponents class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseRepositoryType":
        self.message = f"{self.__class__.__name__}: Invalid _repository input value. It must be a subclass of RepositoryInterface."
        super().__init__(self.message)


class InvalidDatabaseSettingsType(ExceptionWithContext):
    """Exception raised for errors in the input value of settings attribute in the Database class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseSettingsType":
        self.message = f"{self.__class__.__name__}: Invalid settings input value. It must be a DatabaseSettings type."
        super().__init__(self.message)


class InvalidDatabaseComponentsType(ExceptionWithContext):
    """Exception raised for errors in the input value of components attribute in the Database class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseComponentsType":
        self.message = f"{self.__class__.__name__}: Invalid components input value. It must be a DatabaseComponents type."
        super().__init__(self.message)


class InvalidHostType(ExceptionWithContext):
    """Exception raised for errors in the input value of host attribute in DatabaseSettings class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidHostType":
        self.message = f"{self.__class__.__name__}: Invalid host input value. It need to be a string and a valid hostname accordingly RFC 1123 or a valid IP address."
        super().__init__(self.message)


class InvalidPortType(ExceptionWithContext):
    """Exception raised for errors in the input value of port attribute in DatabaseSettings class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidPortType":
        self.message = f"{self.__class__.__name__}: Invalid port input value. It must be an integer."
        super().__init__(self.message)


class InvalidUseSSLType(ExceptionWithContext):
    """Exception raised for errors in the input value of use_ssl attribute in DatabaseSettings class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidUseSSLType":
        self.message = f"{self.__class__.__name__}: Invalid use_ssl input value. It must be a bool."
        super().__init__(self.message)


class InvalidDatabaseType(ExceptionWithContext):
    """Exception raised for errors in the input value of database attribute in DatabaseSettings class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidDatabaseType":
        self.message = f"{self.__class__.__name__}: Invalid database input value. It must be a string."
        super().__init__(self.message)
