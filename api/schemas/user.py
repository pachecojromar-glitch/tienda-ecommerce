from typing import Optional
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    email: str
    password: str

class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None

class UserLogin(SQLModel):
    email: str
    password: str
