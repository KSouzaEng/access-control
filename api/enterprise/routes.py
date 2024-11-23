from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from auth.auth import create_access_token, get_password_hash, verify_password, get_current_user
from enterprise.models import Enterprise
from enterprise.schema import EnterpriseBase,EnterpriseCreate,EnterpriseResponse,EnterpriseUpdate

enterpriseRouter = APIRouter()

@enterpriseRouter.post("/register", response_model=EnterpriseResponse, dependencies=[Depends(get_current_user)])
def register_enterprise(enterprise: EnterpriseCreate, db: Session = Depends(get_db)):
    db_enterprise = Enterprise(name=enterprise.name, contact=enterprise.contact, email=enterprise.email,owner_id=enterprise.owner_id)
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

@enterpriseRouter.put("/{id}", response_model=EnterpriseResponse)
def update_user(id: int, enterprise: EnterpriseUpdate, db: Session = Depends(get_db), current_user: Enterprise = Depends(get_current_user)):
    db_enterprise = db.query(Enterprise).filter(Enterprise.id == id).first()
    
    if not db_enterprise:
        raise HTTPException(status_code=404, detail="enterprise not found")
    
    # Atualizando os campos recebidos
    if enterprise.name:
        db_enterprise.name = enterprise.name
    if enterprise.contact:
        db_enterprise.contact = enterprise.contact
    if enterprise.email:
        db_enterprise.email = enterprise.email
    if enterprise.plan:
        db_enterprise.plan = enterprise.plan
    
    db.commit()
    db.refresh(db_enterprise)
    return db_enterprise 

