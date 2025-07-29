from email.mime import image
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserRole

def get_user_by_email(db: Session,email: str):
    """Retrieve a user by email."""
    return db.query(User).filter(User.email == email).first()

