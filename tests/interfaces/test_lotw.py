import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.interfaces import lotw  # noqa: E402


def test_fetch_qsos():
    with patch('backend.interfaces.lotw.requests.get') as mock_get:
        mock_get.return_value.json.return_value = [{'id': 1}]
        mock_get.return_value.raise_for_status.return_value = None
        result = lotw.fetch_qsos('secret')
        mock_get.assert_called_once()
        assert result == [{'id': 1}]


def test_push_qso():
    with patch('backend.interfaces.lotw.requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'status': 'ok'}
        mock_post.return_value.raise_for_status.return_value = None
        result = lotw.push_qso('secret', {'id': 1})
        mock_post.assert_called_once()
        assert result == {'status': 'ok'}
