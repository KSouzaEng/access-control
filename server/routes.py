from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from server.models import Server
from core.database import get_db
from auth.auth import  get_current_user
from server.schema import ServerCreate,ServerResponse,ServerUpdate

server_router = APIRouter()

@server_router.post("/register", response_model=ServerResponse, dependencies=[Depends(get_current_user)])
def register_enterprise(server: ServerCreate, db: Session = Depends(get_db)):
    db_server = Server(name=server.name, plan_id=server.plan_id)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

@server_router.get("/list", dependencies=[Depends(get_current_user)])
def list_servers(db: Session = Depends(get_db)):
    return db.query(Server).all()

@server_router.get("/{id}", dependencies=[Depends(get_current_user)])
def get_one_server(id:int,db: Session = Depends(get_db)):
    return db.query(Server).filter(Server.id == id).first()

@server_router.delete("/delete/{user_id}", dependencies=[Depends(get_current_user)])
def delete_server(id: int,db: Session = Depends(get_db)):
   server = db.query(Server).filter(Server.id == id).first()
   if server is None:
        raise HTTPException(status_code=404, detail="user not found")
   db.delete(server)
   db.commit()
   return {"msg": "Server deleted"}

@server_router.put("/{id}", response_model=ServerResponse,dependencies=[Depends(get_current_user)])
def update_server_info(id: int, server: ServerUpdate, db: Session = Depends(get_db)):
    db_server = db.query(Server).filter(Server.id == id).first()
    
    if not db_server:
        raise HTTPException(status_code=404, detail="server info not found")
    
    # Atualizando os campos recebidos
    if server.name:
        db_server.name = server.name
    if server.plan_id:
        db_server.plan_id = server.plan_id
 
    db.commit()
    db.refresh(db_server)
    return db_server 

