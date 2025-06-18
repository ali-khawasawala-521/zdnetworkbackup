from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    enable_password = Column(String, nullable=True)
    hostname = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    backups = relationship(
            "Backup",
            back_populates="device",
            cascade="all, delete-orphan"
        )

class Backup(Base):
    __tablename__ = "backups"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    ip_address = Column(String, nullable=False)
    hostname = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    config = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="backups")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")
