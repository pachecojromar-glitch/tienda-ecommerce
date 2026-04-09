from typing import Optional
from sqlmodel import SQLModel

class CommentCreate(SQLModel):
    content: str
    user_id: int
    product_id: int

class CommentUpdate(SQLModel):
    content: Optional[str] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
