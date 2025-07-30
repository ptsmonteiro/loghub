"""Ham365 service API remote."""

from typing import Dict, List
import requests

BASE_URL = "https://example.com/ham365"


def fetch_qsos(api_key: str) -> List[Dict]:
    """Fetch QSOs from Ham365 via HTTP API."""
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(f"{BASE_URL}/qsos", headers=headers)
    resp.raise_for_status()
    return resp.json()


def push_qso(api_key: str, qso: Dict) -> Dict:
    """Push a single QSO record to Ham365."""
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.post(f"{BASE_URL}/qsos", headers=headers, json=qso)
    resp.raise_for_status()
    return resp.json()


def sync_qsos(local_session, api_key: str, push: bool = False) -> None:
    """Synchronize QSOs with Ham365."""

    from sqlalchemy.orm import Session

    from .. import models

    if not isinstance(local_session, Session):
        raise TypeError("local_session must be a sqlalchemy Session")

    remote_qsos = fetch_qsos(api_key)
    for data in remote_qsos:
        qso_id = data.get("id")
        qso = (
            local_session.query(models.RemoteQSO)
            .filter_by(remote_id=qso_id, remote="ham365")
            .first()
        )
        if qso:
            qso.callsign = data.get("callsign")
            qso.frequency = data.get("frequency")
            qso.mode = data.get("mode")
            qso.timestamp = data.get("timestamp")
        else:
            qso = models.RemoteQSO(
                remote_id=qso_id,
                remote="ham365",
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
                api_key,
                {
                    "id": local.id,
                    "callsign": local.callsign,
                    "frequency": local.frequency,
                    "mode": local.mode,
                    "timestamp": local.timestamp,
                },
            )
