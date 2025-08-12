import datetime as dt
import pytest
from django.db.models.deletion import ProtectedError

from qsos.models import QSO, LogImport


@pytest.mark.django_db
def test_qso_can_link_to_upload_and_protects_delete():
    up = LogImport.objects.create(
        kind=LogImport.KIND_FILE,
        format=LogImport.FORMAT_ADIF,
        original_filename="log.adi",
        station_callsign="F4JAW",
    )
    q = QSO.objects.create(
        callsign="K1ABC",
        qso_date=dt.date(2024, 1, 1),
        time_on=dt.time(12, 34, 0),
        band="20m",
        mode="SSB",
        upload=up,
    )
    assert q.upload_id == up.id
    assert up.qsos.count() == 1

    with pytest.raises(ProtectedError):
        up.delete()
