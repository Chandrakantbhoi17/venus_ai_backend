from pydantic import BaseModel, EmailStr,Field
from app.models.enums import UserRole
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role:UserRole

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str

    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., example="oldpassword123")
    new_password: str = Field(..., min_length=8, example="newpassword456")