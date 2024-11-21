from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from user.models import UserCreate, UserResponse
from user.schema import User
from auth.routes import get_password_hash,get_current_user
from core.database import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=UserResponse,dependencies=[Depends(get_current_user)])
def get_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("")
def get_user( db: Session = Depends(get_db)):
    user = db.query(User).all()
    if user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return user

@router.get("/protected-route", dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "Você acessou uma rota protegida!"}

