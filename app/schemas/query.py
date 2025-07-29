from pydantic import BaseModel, EmailStr
from typing import Optional
class QueryCreate(BaseModel):
    name: str
    email: EmailStr
    user_input: str


class QueryRead(QueryCreate):
    id: int
    file_url:Optional[str]=None
    
    class Config:
        orm_mode = True
