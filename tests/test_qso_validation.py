import datetime as dt
import pytest
from decimal import Decimal

from logbook.models import LogEntry as QSO


@pytest.mark.django_db
def test_band_derived_from_freq():
    q = QSO(
        callsign="K1ABC",
        qso_date=dt.date(2024, 1, 1),
        time_on=dt.time(12, 0),
        mode="SSB",
        freq=Decimal("14.074"),
    )
    q.save()
    assert q.band == "20m"


@pytest.mark.django_db
def test_sat_requires_sat_name():
    q = QSO(
        callsign="F4JAW",
        qso_date=dt.date(2024, 1, 1),
        time_on=dt.time(12, 0),
        mode="FM",
        band="2m",
        prop_mode="SAT",
    )
    with pytest.raises(Exception):
        q.save()


@pytest.mark.django_db
def test_callsign_validation_rules():
    q = QSO(
        callsign="/BAD/",
        qso_date=dt.date(2024, 1, 1),
        time_on=dt.time(12, 0),
        mode="SSB",
        band="20m",
    )
    with pytest.raises(Exception):
        q.save()
