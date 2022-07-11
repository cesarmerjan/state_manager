from src.schemas.state import StateSchema


def test_state_schema():
    payload = {"data": "data"}
    subject = "user_id"
    time_to_expire = {"seconds": 5}
    audience = {"hosts": ["127.0.0.1", "www.google.com", "other-service.io"]}
    state_schema = StateSchema(
        payload=payload, subject=subject, timeToExpire=time_to_expire, audience=audience
    )

    assert state_schema


# need to test exceptions
