from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Enterprise(Base):
    __tablename__ = "enterprises"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contact = Column(String, unique=True, index=True)
    email = Column(String)
    owner_id = Column(Integer, ForeignKey("servers.id"))

    owner = relationship("Server")
