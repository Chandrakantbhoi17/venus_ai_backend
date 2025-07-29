from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from .base import Base

class Query(Base):
    __tablename__ = "query"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    user_input = Column(String(500), nullable=True)
    file_url=Column(String(100),nullable=True)

