from typing import Optional,List
from datetime import datetime
from sqlmodel import SQLModel,Field,Relationship

class Category(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str
    slug:str
    image:str
    creationAt:datetime=Field(default_factory=datetime.utcnow)
    updatedAt:datetime=Field(default_factory=datetime.utcnow)
    products:List["Product"]=Relationship(back_populates="category")

class User(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    email:str
    password:str
    comments:List["Comment"]=Relationship(back_populates="user")

class Product(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    title:str
    slug:str
    price:int
    description:str
    images:str
    creationAt:datetime=Field(default_factory=datetime.utcnow)
    updatedAt:datetime=Field(default_factory=datetime.utcnow)
    category_id:int=Field(foreign_key="category.id")
    category:Optional[Category]=Relationship(back_populates="products")
    comments:List["Comment"]=Relationship(back_populates="product")

class Comment(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    content:str
    creationAt:datetime=Field(default_factory=datetime.utcnow)
    user_id:int=Field(foreign_key="user.id")
    product_id:int=Field(foreign_key="product.id")
    user:Optional[User]=Relationship(back_populates="comments")
    product:Optional[Product]=Relationship(back_populates="comments")