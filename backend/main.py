from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from . import remotes

from . import models, schemas
from .database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/qsos", response_model=schemas.QSO)
def create_qso(
    qso: schemas.QSOCreate,
    remote: str | None = None,
    db: Session = Depends(get_db),
):
    model = models.RemoteQSO if remote else models.QSO
    data = qso.dict()
    if remote:
        data["remote"] = remote
    db_qso = model(**data)
    db.add(db_qso)
    db.commit()
    db.refresh(db_qso)
    return db_qso


@app.get("/qsos", response_model=list[schemas.QSO])
def read_qsos(
    skip: int = 0,
    limit: int = 100,
    remote: str | None = None,
    db: Session = Depends(get_db),
):
    model = models.RemoteQSO if remote else models.QSO
    query = db.query(model)
    if remote:
        query = query.filter(model.remote == remote)
    return query.offset(skip).limit(limit).all()


@app.get("/qsos/{qso_id}", response_model=schemas.QSO)
def read_qso(qso_id: int, remote: str | None = None, db: Session = Depends(get_db)):
    model = models.RemoteQSO if remote else models.QSO
    query = db.query(model).filter(model.id == qso_id)
    if remote:
        query = query.filter(model.remote == remote)
    qso = query.first()
    if qso is None:
        raise HTTPException(status_code=404, detail="QSO not found")
    return qso


@app.put("/qsos/{qso_id}", response_model=schemas.QSO)
def update_qso(
    qso_id: int,
    qso_update: schemas.QSOUpdate,
    remote: str | None = None,
    db: Session = Depends(get_db),
):
    model = models.RemoteQSO if remote else models.QSO
    query = db.query(model).filter(model.id == qso_id)
    if remote:
        query = query.filter(model.remote == remote)
    qso = query.first()
    if qso is None:
        raise HTTPException(status_code=404, detail="QSO not found")
    for key, value in qso_update.dict(exclude_unset=True).items():
        setattr(qso, key, value)
    db.commit()
    db.refresh(qso)
    return qso


@app.delete("/qsos/{qso_id}")
def delete_qso(
    qso_id: int,
    remote: str | None = None,
    db: Session = Depends(get_db),
):
    model = models.RemoteQSO if remote else models.QSO
    query = db.query(model).filter(model.id == qso_id)
    if remote:
        query = query.filter(model.remote == remote)
    qso = query.first()
    if qso is None:
        raise HTTPException(status_code=404, detail="QSO not found")
    db.delete(qso)
    db.commit()
    return {"ok": True}


@app.post("/sync/{remote_name}")
def sync_remote(
    remote_name: str,
    push: bool = False,
    api_key: str | None = None,
    username: str | None = None,
    password: str | None = None,
    db: Session = Depends(get_db),
):
    """Synchronize QSOs with a remote service."""

    sync_map = {
        "clublog": remotes.clublog.sync_qsos,
        "lotw": remotes.lotw.sync_qsos,
        "ham365": remotes.ham365.sync_qsos,
        "qrz": remotes.qrz.sync_qsos,
    }

    if remote_name not in sync_map:
        raise HTTPException(status_code=404, detail="Unknown remote")

    sync_func = sync_map[remote_name]

    if remote_name in {"clublog", "lotw", "ham365"}:
        if not api_key:
            raise HTTPException(status_code=400, detail="api_key required")
        sync_func(db, api_key, push=push)
    elif remote_name == "qrz":
        if not username or not password:
            raise HTTPException(
                status_code=400, detail="username and password required"
            )
        sync_func(db, username, password, push=push)

    remote_count = (
        db.query(models.RemoteQSO).filter(models.RemoteQSO.remote == remote_name).count()
    )
    local_count = db.query(models.QSO).count()

    return {
        "remote": remote_name,
        "remote_qsos": remote_count,
        "local_qsos": local_count,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
