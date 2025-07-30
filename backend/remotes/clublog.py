"""Club Log service API remote."""

from typing import Dict, List
import requests

BASE_URL = "https://example.com/clublog"


def fetch_qsos(api_key: str) -> List[Dict]:
    """Fetch QSOs from Club Log via HTTP API."""
    params = {"api_key": api_key}
    resp = requests.get(f"{BASE_URL}/qsos", params=params)
    resp.raise_for_status()
    return resp.json()


def push_qso(api_key: str, qso: Dict) -> Dict:
    """Push a single QSO record to Club Log."""
    params = {"api_key": api_key}
    resp = requests.post(f"{BASE_URL}/qsos", params=params, json=qso)
    resp.raise_for_status()
    return resp.json()


def sync_qsos(local_session, api_key: str, push: bool = False) -> None:
    """Synchronize QSOs with Club Log.

    Remote QSOs are fetched via :func:`fetch_qsos` and stored in the
    ``RemoteQSO`` table. Existing rows (matched by ``id`` and the
    ``remote`` field) are updated while new ones are inserted.  When the
    ``push`` flag is provided, all local ``QSO`` entries are pushed using
    :func:`push_qso`.
    """

    from sqlalchemy.orm import Session

    from .. import models

    if not isinstance(local_session, Session):
        raise TypeError("local_session must be a sqlalchemy Session")

    remote_qsos = fetch_qsos(api_key)
    for data in remote_qsos:
        qso_id = data.get("id")
        qso = (
            local_session.query(models.RemoteQSO)
            .filter_by(id=qso_id, remote="clublog")
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
                remote="clublog",
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
