from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserRole
from app.core.security import hash_password


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, full_name=user.full_name,password=hashed_password,role=UserRole.USER)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
