from functools import lru_cache
from typing import Optional

from src.database.interfaces import (DatabaseManagerInterface,
                                     RepositoryInterface, UnitOfWorkInterface)

from .components import DatabaseComponents
from .exceptions import (InvalidDatabaseComponentsType,
                         InvalidDatabaseSettingsType)
from .settings import DatabaseSettings


class DatabaseFacade:

    __slots__ = (
        "_components",
        "_settings",
        "_database_manager",
    )

    def __init__(
        self, components: DatabaseComponents, settings: DatabaseSettings
    ) -> "DatabaseFacade":
        self._components = None
        self.components = components
        self._settings = None
        self.settings = settings

    @property
    def components(self) -> DatabaseComponents:
        return self._components

    @components.setter
    def components(self, components: DatabaseComponents) -> None:
        if not isinstance(components, DatabaseComponents):
            raise InvalidDatabaseComponentsType
        self._components = components

    @property
    def settings(self) -> DatabaseSettings:
        return self._settings

    @settings.setter
    def settings(self, settings: DatabaseSettings) -> None:
        if not isinstance(settings, DatabaseSettings):
            raise InvalidDatabaseSettingsType

        self._settings = settings

    @property
    @lru_cache()
    def manager(self) -> DatabaseManagerInterface:
        return self.components.manager(**self.settings.to_dict())

    def connect(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 3
    ) -> None:
        return self.manager.connect(
            username,
            password,
            timeout
        )

    def disconnect(self):
        return self.manager.disconnect()

    @property
    def is_connected(self):
        return self.manager.is_connected

    def get_unit_of_work(self) -> UnitOfWorkInterface:
        return self.components.unit_of_work(self.manager.database_client_factory)

    def get_repository(self) -> RepositoryInterface:
        return self.components.repository

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass
