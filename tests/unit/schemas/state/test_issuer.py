from src.schemas.state.issuer import IssuerSchema, optional_host_validator


def test_issuer_schema():
    host = "localhost"
    issuer_schema = IssuerSchema(host=host)
    assert issuer_schema.host == host

    host = "www.google.com"
    issuer_schema = IssuerSchema(host=host)
    assert issuer_schema.host == host

    host = "192.0.0.1"
    issuer_schema = IssuerSchema(host=host)
    assert issuer_schema.host == host


def test_optional_host_validator():
    assert optional_host_validator(None) == "unknown"
    assert optional_host_validator("") == "unknown"
    assert optional_host_validator("127.0.0.1") == "127.0.0.1"
