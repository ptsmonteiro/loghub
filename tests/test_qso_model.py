import datetime as dt

from logbook.models import LogEntry as QSO


def test_qso_str():
    q = QSO(
        callsign="K1ABC",
        qso_date=dt.date(2024, 1, 1),
        time_on=dt.time(12, 34),
        band="20m",
        mode="SSB",
    )
    s = str(q)
    assert "K1ABC" in s and "20m" in s and "SSB" in s
