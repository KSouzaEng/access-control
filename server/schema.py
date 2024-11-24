from pydantic import BaseModel
from typing import Optional

class ServerBase(BaseModel):
    name: str
    plan_id: int

class ServerCreate(ServerBase):
    name: str
    plan_id: int

class ServerUpdate(BaseModel):
    name: Optional[str] = None
    plan_id: Optional[int] = None

class ServerResponse(ServerBase):
    id: int
    name: str
    plan_id: int

    class Config:
        from_attributes = True
