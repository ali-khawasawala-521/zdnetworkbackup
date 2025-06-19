from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from backend import crud, schemas, models
from backend.database import get_db
from io import StringIO

router = APIRouter(prefix="/backup", tags=["Backups"])

@router.get("/", response_model=List[schemas.BackupOut])
def get_all_backups(db: Session = Depends(get_db), user: int = Depends(crud.require_session_user)):
    return crud.get_backups(db)

@router.get("/{backup_id}", response_model=schemas.BackupCFGOut)
def get_backup(backup_id: int, db: Session = Depends(get_db), user: int = Depends(crud.require_session_user)):
    return crud.get_backup(db, backup_id)

@router.get("/device/{device_id}", response_model=List[schemas.BackupOut])
def get_backups_for_device(device_id: int, db: Session = Depends(get_db), user: int = Depends(crud.require_session_user)):
    return crud.get_backup_by_device_id(db, device_id)

@router.get("/download/{backup_id}")
def download_config_file(
    backup_id: int,
    db: Session = Depends(get_db),
    user: int = Depends(crud.require_session_user)
):
    # Fetch the backup entry from the database
    backup = db.query(models.Backup).filter(models.Backup.id == backup_id).first()

    if not backup:
        raise HTTPException(status_code=404, detail="Backup not found")

    # Prepare file-like object in memory
    file_like = StringIO(str(backup.config))

    # Generate filename from hostname or IP
    filename = f"{backup.id}-{backup.hostname or backup.ip_address}.cfg"

    # Return as downloadable file
    return StreamingResponse(
        file_like,
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.delete("/{backup_id}")
def delete_backup(backup_id: int, db: Session = Depends(get_db), user: int = Depends(crud.require_session_user)):
    deleted = crud.delete_backup(db, backup_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Backup not found")
    return {"message": f"Backup with id {backup_id} deleted"}
