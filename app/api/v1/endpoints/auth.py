from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.base import get_db
from app.crud.user import create_user
from app.services.user import get_user_by_email
from datetime import timedelta
from app.schemas import user as user_schema
from app.services import auth as auth_service

router = APIRouter(prefix="/users",tags=["Authentication"])

@router.post("/register", response_model=user_schema.UserOut)
def register(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_in)



@router.post("/token")
def login(user: user_schema.LoginRequest, db: Session = Depends(get_db)) -> dict:
    """Authenticate user by email and password, return JWT if valid."""
    return auth_service.authenticate_user(user,db)

@router.get("/me",response_model=user_schema.UserOut)
def profile(current_user:  User = Depends(auth_service.get_current_user)) -> dict:
    return current_user





# @router.post("/change_password",tags=['Security'])
# def change_password(
#     payload: user_schema.ChangePasswordRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(auth_service.get_current_user)
# ):


#     # Check current password
#     if not verify_password(payload.current_password,current_user.password):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Current password is incorrect"
#         )

#     # Update password
#     current_user.password =hash_password(payload.new_password)
#     db.commit()

#     return {"message": "Password changed successfully"}
    
   




