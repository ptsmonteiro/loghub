import datetime as dt

import pytest

from decimal import Decimal
from qsos.adif import qso_to_adif, queryset_to_adif
from qsos.models import QSO


@pytest.mark.django_db
def test_single_qso_adif_tags(client):
    q = QSO.objects.create(
        callsign="K1ABC",
        qso_date=dt.date(2024, 1, 1),
        time_on=dt.time(12, 34, 56),
        mode="SSB",
        freq=Decimal("14.074"),
    )
    s = qso_to_adif(q)
    assert "<CALL:" in s and "K1ABC" in s
    assert "<QSO_DATE:8>20240101" in s
    assert "<TIME_ON:6>123456" in s
    assert s.endswith("<EOR>\n")


@pytest.mark.django_db
def test_export_view(client):
    QSO.objects.create(
        callsign="F4JAW",
        qso_date=dt.date(2024, 2, 2),
        time_on=dt.time(6, 7, 8),
        band="20m",
        mode="FT8",
    )
    resp = client.get("/qsos/export.adif")
    assert resp.status_code == 200
    body = resp.content.decode()
    assert "<ADIF_VER:" in body and body.strip().endswith("<EOR>")
