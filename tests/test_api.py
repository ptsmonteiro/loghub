import os
import sys
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import Base  # noqa: E402
from backend.main import app, get_db  # noqa: E402


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=sqlalchemy.pool.StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_and_list_qsos(client):
    ts = datetime.utcnow().isoformat()
    local = {"callsign": "TEST", "frequency": 14.0, "mode": "CW", "timestamp": ts}
    remote = {"callsign": "REMOTE", "frequency": 7.0, "mode": "SSB", "timestamp": ts}

    resp = client.post("/qsos", json=local)
    assert resp.status_code == 200
    resp = client.post("/qsos?remote=lotw", json=remote)
    assert resp.status_code == 200

    resp = client.get("/qsos")
    assert len(resp.json()) == 1
    assert resp.json()[0]["callsign"] == "TEST"

    resp = client.get("/qsos?remote=lotw")
    assert len(resp.json()) == 1
    assert resp.json()[0]["callsign"] == "REMOTE"


def test_update_qso(client):
    ts = datetime.utcnow().isoformat()
    data = {"callsign": "OLD", "frequency": 14.0, "mode": "CW", "timestamp": ts}
    resp = client.post("/qsos", json=data)
    assert resp.status_code == 200

    resp = client.put(
        "/qsos/1",
        json={
            "callsign": "NEW",
            "frequency": 14.0,
            "mode": "CW",
            "timestamp": ts,
        },
    )
    assert resp.status_code == 200
    assert resp.json()["callsign"] == "NEW"

    resp = client.get("/qsos/1")
    assert resp.json()["callsign"] == "NEW"


def test_delete_qso(client):
    ts = datetime.utcnow().isoformat()
    data = {"callsign": "DEL", "frequency": 14.0, "mode": "CW", "timestamp": ts}
    resp = client.post("/qsos", json=data)
    assert resp.status_code == 200

    resp = client.delete("/qsos/1")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True

    resp = client.get("/qsos")
    assert resp.json() == []
