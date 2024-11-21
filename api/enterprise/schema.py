from sqlalchemy import Column, Integer, String
from core.database import Base
from pydantic import BaseModel
from typing import Optional


class EnterpriseBase(BaseModel):
  name: str
  contact: str
  email: str
  plan: str
  
class EnterpriseCreate(EnterpriseBase):
    name: str
    contact: str
    email: str
    plan: str

class EnterpriseResponse(EnterpriseBase):
    id: int
    name: str
    contact: str
    email: str
    plan: str

    class Config:
        from_attributes = True
