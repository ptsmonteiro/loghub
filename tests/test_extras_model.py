import datetime as dt
import pytest

from logbook.models import LogEntry as QSO, LogEntryExtras as QSOExtras
from logbook.adif import entry_to_adif as qso_to_adif


@pytest.mark.django_db
def test_qso_extras_saved_and_exported():
    q = QSO.objects.create(
        callsign="K1EXT",
        qso_date=dt.date(2024, 5, 5),
        time_on=dt.time(10, 20, 30),
        band="20m",
        mode="SSB",
    )
    QSOExtras.objects.create(entry=q, data={"IOTA": "EU-005", "SUBMODE": "JS8"})
    s = qso_to_adif(q)
    assert "<IOTA:6>EU-005" in s
    assert "<SUBMODE:3>JS8" in s
