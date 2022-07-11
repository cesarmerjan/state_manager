from datetime import timedelta

from src.schemas.state.timedelta import TimeDeltaSchema


def test_timedelta_schema():
    dt = TimeDeltaSchema(days=1, hours=1, minutes=2, seconds=3)

    assert timedelta(**dt.dict(exclude_unset=True))

    dt = TimeDeltaSchema(hours=1)

    assert timedelta(**dt.dict(exclude_unset=True))
