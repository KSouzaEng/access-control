from pydantic import BaseModel
from typing import Optional

class PlanBase(BaseModel):
    name: str
    duration: str

class PlanCreate(PlanBase):
    name: str
    duration: str

class PlanUpdate(BaseModel):
    name: Optional[str] = None
    duration: Optional[str] = None

class PlanResponse(PlanBase):
    id: int
    name: str
    duration: str

    class Config:
        from_attributes = True
