from pydantic import BaseModel, ConfigDict, Extra
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    ip_address: str
    username: str
    password: str
    enable_password: Optional[str] = None
    device_type: str

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    ip_address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    enable_password: Optional[str] = None
    device_type: Optional[str] = None

class DeviceOut(BaseModel):
    id: int
    ip_address: str
    username: str
    device_type: str
    hostname: str
    created_at: datetime
    total_backups: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True, extra=Extra.allow)

class DeviceResponse(BaseModel):
    message: str
    device: DeviceOut

# Backup Schemas
class BackupBase(BaseModel):
    id: int
    device_id: int
    device_type: str
    ip_address: str
    hostname: str
    created_at: datetime

class BackupCreate(BackupBase):
    pass

class BackupOut(BackupBase):
    pass

class BackupResponse(BaseModel):
    message: str
    backup: BackupOut

class BackupCFGOut(BackupBase):
    config: str

    model_config = ConfigDict(from_attributes=True, extra=Extra.allow)
