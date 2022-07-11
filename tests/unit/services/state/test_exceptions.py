from src.services.state.exceptions import (InvalidIssuerType,
                                           InvalidPayloadType,
                                           InvalidRequesterType,
                                           InvalidSecretKeyType,
                                           InvalidSignedStateType,
                                           InvalidSignStateType,
                                           InvalidStateDataType,
                                           InvalidStateType,
                                           InvalidStateUuidType,
                                           InvalidTimeToExpireType,
                                           InvalidUnitOfWorkType,
                                           MissingSecretKey, NotTheAudience,
                                           StateNotFound)


def test_invalid_state_data_type():
    error = InvalidStateDataType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_issuer_type():
    error = InvalidIssuerType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_playload_type():
    error = InvalidPayloadType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_state_type():
    error = InvalidStateType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_state_uuid_type():
    error = InvalidStateUuidType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_time_to_expire_type():
    error = InvalidTimeToExpireType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_unit_of_work_type():
    error = InvalidUnitOfWorkType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_state_not_found():
    error = StateNotFound()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_not_the_audience():
    error = NotTheAudience()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_missing_secret_key():
    error = MissingSecretKey()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_requester_type():
    error = InvalidRequesterType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_secret_key_type():
    error = InvalidSecretKeyType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_sign_state_type():
    error = InvalidSignStateType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_signed_state_type():
    error = InvalidSignedStateType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)
