import datetime as dt
import pytest

from logbook.adif import entry_to_adif as qso_to_adif
from logbook.models import LogEntry as QSO


@pytest.mark.django_db
def test_pota_fields_emit_sig_and_dedicated_tags():
    q = QSO.objects.create(
        callsign="K0POTA",
        qso_date=dt.date(2024, 3, 3),
        time_on=dt.time(10, 0, 0),
        band="20m",
        mode="SSB",
        my_sig="POTA",
        my_sig_info="K-1234",
        sig="POTA",
        sig_info="K-4321",
    )
    adif = qso_to_adif(q)
    assert "<MY_SIG:4>POTA" in adif
    assert "<MY_SIG_INFO:6>K-1234" in adif
    assert "<SIG:4>POTA" in adif
    assert "<SIG_INFO:6>K-4321" in adif


@pytest.mark.django_db
def test_sota_fields_emit_sig_and_dedicated_tags():
    q = QSO.objects.create(
        callsign="G0SOTA",
        qso_date=dt.date(2024, 4, 4),
        time_on=dt.time(11, 11, 11),
        band="40m",
        mode="CW",
        my_sota_ref="G/SP-015",
        sota_ref="G/SP-013",
    )
    adif = qso_to_adif(q)
    assert "<MY_SIG:4>SOTA" in adif
    assert "<MY_SIG_INFO:8>G/SP-015" in adif
    assert "<SIG:4>SOTA" in adif
    assert "<SIG_INFO:8>G/SP-013" in adif
    assert "<MY_SOTA_REF:8>G/SP-015" in adif
    assert "<SOTA_REF:8>G/SP-013" in adif
