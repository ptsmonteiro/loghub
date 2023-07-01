import datetime as dt

import pytest
from django.urls import reverse

from qsos.models import QSO


@pytest.mark.django_db
def test_list_view_status_code(client):
    url = reverse("qsos:list")
    resp = client.get(url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_qso_flow(client):
    url = reverse("qsos:create")
    payload = {
        "callsign": "K1ABC",
        "qso_date": dt.date(2024, 1, 1).isoformat(),
        "time_on": dt.time(12, 34).isoformat(timespec="minutes"),
        "band": "20m",
        "mode": "SSB",
    }
    resp = client.post(url, data=payload, follow=False)
    assert resp.status_code in (302, 303)
    assert QSO.objects.count() == 1

