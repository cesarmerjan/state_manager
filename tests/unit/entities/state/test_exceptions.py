from src.entities.state.exceptions import (InvalidAudienceType,
                                           InvalidIssuerType,
                                           InvalidPayloadType,
                                           InvalidSubjectType,
                                           InvalidTimeToExpireType)


def test_invalid_state_payload_type():
    error = InvalidPayloadType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_state_subject_type():
    error = InvalidSubjectType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_state_issuer_type():
    error = InvalidIssuerType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_state_time_to_expire_type():
    error = InvalidTimeToExpireType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)


def test_invalid_state_audience_type():
    error = InvalidAudienceType()
    assert error.context
    assert error.message
    assert isinstance(str(error), str)
