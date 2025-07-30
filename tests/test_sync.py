import os
import sys
from unittest.mock import patch
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend import models  # noqa: E402
from backend.database import Base  # noqa: E402
from backend.remotes import clublog, lotw, ham365, qrz  # noqa: E402


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.mark.parametrize("module,args,remote", [
    (clublog, ("key",), "clublog"),
    (lotw, ("secret",), "lotw"),
    (ham365, ("secret",), "ham365"),
    (qrz, ("user", "pass"), "qrz"),
])
def test_sync_qsos_writes_rows(db_session, module, args, remote):
    first = {
        "id": 1,
        "callsign": "TEST",
        "frequency": 14.0,
        "mode": "CW",
        "timestamp": datetime.utcnow(),
    }
    second = {
        "id": 1,
        "callsign": "NEW",
        "frequency": 7.0,
        "mode": "SSB",
        "timestamp": datetime.utcnow(),
    }

    with patch(f"backend.remotes.{remote}.fetch_qsos", return_value=[first]) as fetch, \
         patch(f"backend.remotes.{remote}.push_qso") as push:
        module.sync_qsos(db_session, *args, push=False)
        fetch.assert_called_once()
        push.assert_not_called()

    rows = db_session.query(models.RemoteQSO).filter_by(remote=remote).all()
    assert len(rows) == 1
    row = rows[0]
    assert row.callsign == "TEST"
    assert row.frequency == 14.0
    assert row.mode == "CW"

    with patch(f"backend.remotes.{remote}.fetch_qsos", return_value=[second]):
        module.sync_qsos(db_session, *args, push=False)

    rows = db_session.query(models.RemoteQSO).filter_by(remote=remote).all()
    assert len(rows) == 1
    row = rows[0]
    assert row.callsign == "NEW"
    assert row.frequency == 7.0
    assert row.mode == "SSB"
