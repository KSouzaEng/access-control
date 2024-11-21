from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from auth.auth import create_access_token, get_password_hash, verify_password, get_current_user
from enterprise.models import Enterprise
from enterprise.schema import EnterpriseBase,EnterpriseCreate,EnterpriseResponse

enterpriseRouter = APIRouter()

@enterpriseRouter.post("/register", response_model=EnterpriseResponse, dependencies=[Depends(get_current_user)])
def register_enterprise(enterprise: EnterpriseCreate, db: Session = Depends(get_db)):
    db_enterprise = Enterprise(name=enterprise.name, contact=enterprise.contact, email=enterprise.email,plan=enterprise.plan)
    db.add(db_enterprise)
    db.commit()
    db.refresh(db_enterprise)
    return db_enterprise

@enterpriseRouter.get("/enterprises", dependencies=[Depends(get_current_user)])
def list_enterprises(db: Session = Depends(get_db)):
    return db.query(Enterprise).all()

@enterpriseRouter.get("/enterprise/{id}", dependencies=[Depends(get_current_user)])
def get_one_enterprise(id:int,db: Session = Depends(get_db)):
    return db.query(Enterprise).filter(Enterprise.id == id).first()

@enterpriseRouter.delete("/delete/{user_id}", dependencies=[Depends(get_current_user)])
def delete_enterprise(id: int,db: Session = Depends(get_db)):
   enterprise = db.query(Enterprise).filter(Enterprise.id == id).first()
   if enterprise is None:
        raise HTTPException(status_code=404, detail="user not found")
   db.delete(enterprise)
   db.commit()
   return {"msg": "Enterprise deleted"}

# @router.put("/users/{user_id}", response_model=UserOut)
# def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_user = db.query(User).filter(User.id == user_id).first()
    
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Atualizando os campos recebidos
#     if user.username:
#         db_user.username = user.username
#     if user.email:
#         db_user.email = user.email
#     if user.password:
#         db_user.hashed_password = get_password_hash(user.password)
    
#     db.commit()
#     db.refresh(db_user)
#     return db_user 

