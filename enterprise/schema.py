from sqlalchemy import Column, Integer, String
from core.database import Base
from pydantic import BaseModel
from typing import Optional


class EnterpriseBase(BaseModel):
  name: str
  contact: str
  email: str
  owner_id:int
  
class EnterpriseCreate(EnterpriseBase):
    name: str
    contact: str
    email: str
    owner_id:int


class EnterpriseUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None

class EnterpriseResponse(EnterpriseBase):
    id: int
    name: str
    contact: str
    email: str
    owner_id: int


    class Config:
        from_attributes = True
