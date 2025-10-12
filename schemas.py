# schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        orm_mode = True

class ChatCreate(BaseModel):
    user_id: Optional[int] = None
    message: str

class ChatOut(BaseModel):
    id: int
    user_id: Optional[int]
    message: str
    reply: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True
