from typing import Optional
from sqlmodel import SQLModel

class ProductCreate(SQLModel):
    title:str
    slug:str
    price:int
    description:str
    images:str
    category_id:int

class ProductUpdate(SQLModel):
    title:Optional[str]=None
    slug:Optional[str]=None
    price:Optional[int]=None
    description:Optional[str]=None
    images:Optional[str]=None
    category_id:Optional[int]=None