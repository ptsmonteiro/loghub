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
