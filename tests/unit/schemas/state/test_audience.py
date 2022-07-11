from src.schemas.state.audience import AudienceSchema


def test_audience_schema():
    audience_schema = AudienceSchema(
        hosts=[
            "pydantic-docs.helpmanual.io",
            "localhost",
            "www.google.com",
        ]
    )

    assert audience_schema.hosts == [
        "pydantic-docs.helpmanual.io",
        "localhost",
        "www.google.com",
    ]
