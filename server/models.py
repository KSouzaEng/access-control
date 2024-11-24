from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship

## add model server
class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))

    plan = relationship("Plan")
