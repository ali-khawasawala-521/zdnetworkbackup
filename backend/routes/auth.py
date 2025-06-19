from fastapi import APIRouter, Depends, Response, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend import crud, database

router = APIRouter()

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login_user(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    user = crud.login_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = crud.create_session(db, user.id).token

    # Set session cookie
    response.set_cookie(
        key="session_token",
        value=str(token),  # Use a session token in production
        httponly=False,  # Set to True in production for security
        max_age=86400,  # 1 day
        samesite="lax",
        secure=False  # use False only for localhost testing
    )

    return {"message": "Login successful", "user_id": user.id}

@router.post("/logout")
def logout_user(response: Response, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session_token")
    if token:
        crud.delete_session(db, token)
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}

@router.get("/verify-user")
def verify_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No session found")

    session = crud.get_session(db, token)
    user = db.query(crud.models.User).filter_by(id=session.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "message": "User verified"
    }

@router.get("/me")
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = crud.get_session(db, token)
    user = db.query(crud.models.User).filter_by(id=session.user_id).first()
    return {"user": user}
