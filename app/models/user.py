# app/models/user.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False,default=UserRole.USER)
    password = Column(String, nullable=False)
  