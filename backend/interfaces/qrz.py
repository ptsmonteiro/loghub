"""QRZ.com service API interface."""

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
