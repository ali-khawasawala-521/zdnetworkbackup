import os
import sqlite3
from passlib.context import CryptContext

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DB_PATH = os.path.join(BASE_DIR, "data.db")
DATABASE_URL = f"sqlite:///{DATA_DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"])

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(email: str):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(email: str, password: str):
    hashed_pw = pwd_context.hash(password)
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT)")
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
    conn.commit()
    conn.close()

def verify_user(email: str, password: str) -> bool:
    user = get_user(email)
    if user and pwd_context.verify(password, user[2]):
        return True
    return False
