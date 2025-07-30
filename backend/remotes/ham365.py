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
