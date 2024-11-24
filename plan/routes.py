from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from plan.models import Plan
from core.database import get_db
from auth.auth import  get_current_user
from plan.schema import PlanResponse,PlanCreate,PlanUpdate

plan_router = APIRouter()

@plan_router.post("/register", response_model=PlanResponse, dependencies=[Depends(get_current_user)])
def register_enterprise(plan: PlanCreate, db: Session = Depends(get_db)):
    db_plan = Plan(name=plan.name, duration=plan.duration)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

#get list plans
@plan_router.get("/", dependencies=[Depends(get_current_user)])
def list_plans(db: Session = Depends(get_db)):
    return db.query(Plan).all()

@plan_router.get("/{plan_id}", dependencies=[Depends(get_current_user)])
def get_one_plan(plan_id:int,db: Session = Depends(get_db)):
    return db.query(Plan).filter(Plan.id == plan_id).first()

@plan_router.delete("/{plan_id}", dependencies=[Depends(get_current_user)])
def delete_plan(plan_id:int,db: Session = Depends(get_db)):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(db_plan)
    db.commit()
    return {"msg": "Plan deleted"}

@plan_router.put("/{id}", response_model=PlanResponse)
def update_user(id: int, plan: PlanUpdate, db: Session = Depends(get_db), current_user: Plan = Depends(get_current_user)):
    db_plan = db.query(Plan).filter(Plan.id == id).first()
    
    if not db_plan:
        raise HTTPException(status_code=404, detail="plan not found")
    
    # Atualizando os campos recebidos
    if plan.name:
        db_plan.name = plan.name
    if plan.duration:
        db_plan.duration = plan.duration
    
    db.commit()
    db.refresh(db_plan)
    return db_plan 



