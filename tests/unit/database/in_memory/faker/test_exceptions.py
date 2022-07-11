from src.database.in_memory.faker.exceptions import (InvalidKeyOrValueType,
                                                     InvalidKeyType)


def test_invalid_key_or_value_type():
    error = InvalidKeyOrValueType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_key_type():
    error = InvalidKeyType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)
