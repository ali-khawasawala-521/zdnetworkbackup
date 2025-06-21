import os
import json
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING
from backend.logger import logger
from backend.crud import get_devices, create_backup
from backend.database import get_context_db

scheduler = BackgroundScheduler()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "scheduler_state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"active": False, "last_run": None}

def save_state(active, last_run):
    state = {"active": active, "last_run": last_run}
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def backup_job():
    utc_now = datetime.now(timezone.utc).isoformat()
    logger.info(f"Scheduled backup started at {utc_now}")
    try:
        with get_context_db() as db:
            devices = get_devices(db)
            for device in devices:
                logger.info(f"Backing up device {device.id}:{device.hostname}:{device.ip_address}")
                create_backup(db, device.id)
        logger.info("Backup completed successfully.")
        save_state(True, utc_now)
    except Exception as e:
        logger.error(f"Scheduled backup failed: {e}")

def start_scheduler():
    state = load_state()
    if scheduler.state != STATE_RUNNING:
        scheduler.start()

    if state.get("active"):
        if not scheduler.get_job("backup_task"):
            scheduler.add_job(
                backup_job,
                trigger="cron",
                day_of_week="sun",
                hour=2,
                minute=0,
                id="backup_task",
                replace_existing=True
            )
        logger.info("Scheduler restarted and job resumed.")
    else:
        logger.info("Scheduler loaded but job is inactive.")
