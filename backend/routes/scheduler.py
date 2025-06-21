from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import crud
from backend.scheduler import scheduler, load_state, save_state, start_scheduler
from backend.database import get_db

router = APIRouter()
router = APIRouter(prefix="/scheduler", tags=["Scheduler"])

@router.post("/start")
def start(
    db: Session = Depends(get_db),
    session = Depends(crud.require_session_user)
):
    if not scheduler.get_job("backup_task"):
        start_scheduler()
        save_state(True, None)
        return {"message": "Scheduler started", "status": "active"}
    return {"message": "Scheduler already running", "status": "active"}

@router.post("/stop")
def stop(
    db: Session = Depends(get_db),
    session = Depends(crud.require_session_user)
):
    job = scheduler.get_job("backup_task")
    if job:
        job.remove()
    save_state(False, None)
    return {"message": "Scheduler stopped", "status": "inactive"}

@router.get("/status")
def status(
    db: Session = Depends(get_db),
    session = Depends(crud.require_session_user)
):
    return load_state()
