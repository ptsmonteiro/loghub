"""QRZ.com service API remote."""

from typing import Dict, List
import requests

BASE_URL = "https://example.com/qrz"


def fetch_qsos(username: str, password: str) -> List[Dict]:
    """Fetch QSOs from QRZ.com via HTTP API."""
    resp = requests.get(
        f"{BASE_URL}/qsos",
        params={"user": username, "password": password},
    )
    resp.raise_for_status()
    return resp.json()


def push_qso(username: str, password: str, qso: Dict) -> Dict:
    """Push a single QSO record to QRZ.com."""
    resp = requests.post(
        f"{BASE_URL}/qsos",
        params={"user": username, "password": password},
        json=qso,
    )
    resp.raise_for_status()
    return resp.json()


def sync_qsos(local_session, username: str, password: str, push: bool = False) -> None:
    """Synchronize QSOs with QRZ.com."""

    from sqlalchemy.orm import Session

    from .. import models

    if not isinstance(local_session, Session):
        raise TypeError("local_session must be a sqlalchemy Session")

    remote_qsos = fetch_qsos(username, password)
    for data in remote_qsos:
        qso_id = data.get("id")
        qso = (
            local_session.query(models.RemoteQSO)
            .filter_by(id=qso_id, remote="qrz")
            .first()
        )
        if qso:
            qso.callsign = data.get("callsign")
            qso.frequency = data.get("frequency")
            qso.mode = data.get("mode")
            qso.timestamp = data.get("timestamp")
        else:
            qso = models.RemoteQSO(
                id=qso_id,
                remote="qrz",
                callsign=data.get("callsign"),
                frequency=data.get("frequency"),
                mode=data.get("mode"),
                timestamp=data.get("timestamp"),
            )
            local_session.add(qso)

    local_session.commit()

    if push:
        for local in local_session.query(models.QSO).all():
            push_qso(
                username,
                password,
                {
                    "id": local.id,
                    "callsign": local.callsign,
                    "frequency": local.frequency,
                    "mode": local.mode,
                    "timestamp": local.timestamp,
                },
            )
