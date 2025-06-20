from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend import models, schemas
from backend.database import get_db
from backend.device import get_netmiko_connection, get_device_backup, get_device_hostname
import secrets
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- Users ----
def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = models.User(email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and pwd_context.verify(password, str(user.password)):
        return user
    return None

def verify_user(db: Session, email: str, password: str) -> bool:
    user = get_user(db, email)
    if user and pwd_context.verify(password, str(user.password)):
        return True
    return False

# --- Sessions ---

def create_session(db: Session, user_id: int):
    token = secrets.token_urlsafe(32)
    expire_at = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    session = models.Session(user_id=user_id, token=token, expires_at=expire_at)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_session(db: Session, token: str):
    session = db.query(models.Session).filter(models.Session.token == token).first()
    if session:
        is_active = datetime.datetime.utcnow() < session.expires_at
        user = get_user_by_id(db, session.user_id)
        if (user and bool(is_active)):
            return session

    raise HTTPException(status_code=401, detail="Unauthorized")

def delete_session(db: Session, token: str):
    session = db.query(models.Session).filter(models.Session.token == token).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False

def delete_all_sessions_for_user(db: Session, user_id: int):
    sessions = db.query(models.Session).filter(models.Session.user_id == user_id).all()
    for session in sessions:
        db.delete(session)
    db.commit()
    return True

# -- Verify session user --
def require_session_user(request: Request, db: Session = Depends(get_db)):
    for key in request.cookies:
        if key.startswith("session_token"):
            session_token = request.cookies.get(key)
            if (session_token):
                return get_session(db, session_token).user_id
    raise HTTPException(status_code=401, detail="Unauthorized")

#  --- Devices and Backups ---
def create_device_with_auto_backup(db: Session, device: schemas.DeviceCreate):
    device_data = device.dict()

    connection = get_netmiko_connection(device_data)
    config = get_device_backup(connection, device_data['device_type'])
    hostname = get_device_hostname(connection, device_data['device_type'])

    device_data.update({
        "hostname": hostname,
    })
    db_device = models.Device(**device_data)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    derived_backup = models.Backup(
        device_id=db_device.id,
        device_type=db_device.device_type,
        ip_address=db_device.ip_address,
        hostname=hostname,
        config=config,
    )

    db.add(derived_backup)
    db.commit()
    db.refresh(derived_backup)

    return db_device

# ---- Devices ----

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    devices = db.query(models.Device).offset(skip).limit(limit).all()
    for device in devices:
        device.total_backups = db.query(models.Backup).filter(models.Backup.device_id == device.id).count()
    return devices

def update_device(db: Session, device_id: int, device_update: schemas.DeviceUpdate):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        return None
    for field, value in device_update.dict(exclude_unset=True).items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device

def delete_device(db: Session, device_id: int):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if device:
        db.delete(device)
        db.commit()
    return device

# ---- Backups ----

def create_backup(db: Session, device_id: int):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not db_device:
        return None

    connection = get_netmiko_connection(db_device.__dict__)
    config = get_device_backup(connection, db_device.device_type)
    hostname = get_device_hostname(connection, db_device.device_type)

    db_backup = models.Backup(
        device_id=db_device.id,
        device_type=db_device.device_type,
        ip_address=db_device.ip_address,
        hostname=hostname,
        config=config,
    )
    db.add(db_backup)
    db.commit()
    db.refresh(db_backup)
    return db_backup

def get_backup(db: Session, backup_id: int):
    return db.query(models.Backup).filter(models.Backup.id == backup_id).first()

def get_backups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Backup).offset(skip).limit(limit).all()

def get_backup_by_device_id(db: Session, device_id: int):
    return db.query(models.Backup).filter(models.Backup.device_id == device_id).all()

def delete_backup(db: Session, backup_id: int):
    backup = db.query(models.Backup).filter(models.Backup.id == backup_id).first()
    if backup:
        db.delete(backup)
        db.commit()
    return backup
