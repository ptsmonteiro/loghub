"""LoTW service API interface."""

from typing import Dict, List
import requests

BASE_URL = "https://example.com/lotw"


def fetch_qsos(api_key: str) -> List[Dict]:
    """Fetch QSOs from LoTW via HTTP API."""
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(f"{BASE_URL}/qsos", headers=headers)
    resp.raise_for_status()
    return resp.json()


def push_qso(api_key: str, qso: Dict) -> Dict:
    """Push a single QSO record to LoTW."""
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.post(f"{BASE_URL}/qsos", headers=headers, json=qso)
    resp.raise_for_status()
    return resp.json()
