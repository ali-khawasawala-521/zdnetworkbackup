from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import schemas, crud
from backend.database import get_db

router = APIRouter()

router = APIRouter(prefix="/device", tags=["Devices"])

@router.post("/", response_model=schemas.DeviceOut)
def create_device(
    device: schemas.DeviceCreate,
    db: Session = Depends(get_db),
    session = Depends(crud.require_session_user)
):
    return crud.create_device_with_auto_backup(db, device)

@router.post("/{device_id}/backup", response_model=schemas.BackupOut)
def create_backup(
    device_id: int,
    db: Session = Depends(get_db),
    session = Depends(crud.require_session_user)
):
    return crud.create_backup(db, device_id)

@router.get("/list", response_model=List[schemas.DeviceOut])
def read_all(db: Session = Depends(get_db), session = Depends(crud.require_session_user)):
    return crud.get_devices(db)

@router.get("/{device_id}", response_model=schemas.DeviceOut)
def read_one(device_id: int, db: Session = Depends(get_db), session = Depends(crud.require_session_user)):
    device = crud.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=schemas.DeviceOut)
def update(device_id: int, device: schemas.DeviceUpdate, db: Session = Depends(get_db), session = Depends(crud.require_session_user)):
    updated = crud.update_device(db, device_id, device)
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated

@router.delete("/{device_id}")
def delete(device_id: int, db: Session = Depends(get_db), session = Depends(crud.require_session_user)):
    deleted = crud.delete_device(db, device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": f"Device {device_id} deleted"}
