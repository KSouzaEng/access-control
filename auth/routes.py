from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from auth.auth import create_access_token, get_password_hash, verify_password, get_current_user
from auth.models import User, Post
from auth.schema import UserCreate,UserUpdate, UserOut, PostCreate, PostOut
from auth.auth import user_dependency
# from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users", dependencies=[Depends(get_current_user)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/user/delete/{user_id}", dependencies=[Depends(get_current_user)])
def delete_user(user_id: int, user: user_dependency,db: Session = Depends(get_db)):
   user = db.query(User).filter(User.id == user_id).filter(User.id == user_id).first()
   if user is None:
        raise HTTPException(status_code=404, detail="user not found")
   db.delete(user)
   db.commit()
   return {"msg": "User deleted"}

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Atualizando os campos recebidos
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user 

@router.post("/posts", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = Post(**post.dict(), owner_id=current_user.id)
    db.add(db_post)
    db.commit()