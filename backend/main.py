from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
def create_qso(qso: schemas.QSOCreate, db: Session = Depends(get_db)):
    db_qso = models.QSO(**qso.dict())
    db.add(db_qso)
    db.commit()
    db.refresh(db_qso)
    return db_qso


@app.get("/qsos", response_model=list[schemas.QSO])
def read_qsos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.QSO).offset(skip).limit(limit).all()


@app.get("/qsos/{qso_id}", response_model=schemas.QSO)
def read_qso(qso_id: int, db: Session = Depends(get_db)):
    qso = db.query(models.QSO).filter(models.QSO.id == qso_id).first()
    if qso is None:
        raise HTTPException(status_code=404, detail="QSO not found")
    return qso


@app.put("/qsos/{qso_id}", response_model=schemas.QSO)
def update_qso(
    qso_id: int,
    qso_update: schemas.QSOUpdate,
    db: Session = Depends(get_db),
):
    qso = db.query(models.QSO).filter(models.QSO.id == qso_id).first()
    if qso is None:
        raise HTTPException(status_code=404, detail="QSO not found")
    for key, value in qso_update.dict(exclude_unset=True).items():
        setattr(qso, key, value)
    db.commit()
    db.refresh(qso)
    return qso


@app.delete("/qsos/{qso_id}")
def delete_qso(qso_id: int, db: Session = Depends(get_db)):
    qso = db.query(models.QSO).filter(models.QSO.id == qso_id).first()
    if qso is None:
        raise HTTPException(status_code=404, detail="QSO not found")
    db.delete(qso)
    db.commit()
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
