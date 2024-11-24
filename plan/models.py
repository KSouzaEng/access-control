
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    duration = Column(String, unique=True, index=True)
