from datetime import datetime, timedelta
from threading import RLock
from typing import Dict, Union

from src.extensions.singleton import MetaSingleton

from .exceptions import InvalidKeyOrValueType, InvalidKeyType


class Faker(metaclass=MetaSingleton):
    """The Faker instance with be like a database session

    Args:
        Borg (_type_): _description_

    Raises:
        InvalidKeyOrValueType: _description_
        InvalidKeyType: _description_

    Returns:
        _type_: _description_
    """

    __slots__ = ("_locker", "_expirations", "database")

    def __init__(self) -> "Faker":
        self._locker: RLock = RLock()
        self._expirations: Dict[str, datetime] = {}
        self.database: Dict[str, str] = {}

    def start_transaction(self) -> None:
        self._locker.acquire()

    def end_transaction(self) -> None:
        self._locker.release()

    def rollback_transaction(self) -> None:
        self._locker.release()

    def _expired(self, key: str) -> bool:
        if self._expirations.get(key):
            if self._expirations[key] < datetime.now():
                del self._expirations[key]
                del self.database[key]
                return True

    def set(self, key: str, value: str) -> None:
        if not isinstance(key, str) or not isinstance(value, str):
            raise InvalidKeyOrValueType

        self.database[key] = value
        self._expirations[key] = datetime.now() + timedelta(days=15)

    def get(self, key: str) -> Union[None, str]:
        if not isinstance(key, str):
            raise InvalidKeyType

        if not self._expired(key):
            return self.database.get(key)
        else:
            return None

    def delete(self, key: str) -> None:
        if not isinstance(key, str):
            raise InvalidKeyType
        if self.database.get(key):
            del self.database[key]
        if self._expirations.get(key):
            del self._expirations[key]

    def exists(self, key: str) -> bool:
        if not isinstance(key, str):
            raise InvalidKeyType

        if self._expired(key):
            return False

        if self.database.get(key):
            return True
        else:
            return False

    def expire(self, key: str, time: timedelta) -> None:
        if not isinstance(key, str):
            raise InvalidKeyType
        self._expirations[key] = datetime.now() + time
