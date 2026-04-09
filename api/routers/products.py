from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session,select
from sqlalchemy.orm import selectinload
from db import get_session
from models import Product,Comment
from schemas.product import ProductCreate,ProductUpdate

router=APIRouter(prefix="/products",tags=["products"])

@router.get("/",response_model=list[Product])
def get_products(session:Session=Depends(get_session)):
    statement=select(Product).options(selectinload(Product.category),selectinload(Product.comments).selectinload(Comment.user))
    return session.exec(statement).all()

@router.get("/{product_id}",response_model=Product)
def get_product(product_id:int,session:Session=Depends(get_session)):
    statement=select(Product).where(Product.id==product_id).options(selectinload(Product.category),selectinload(Product.comments).selectinload(Comment.user))
    product=session.exec(statement).first()
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    return product

@router.post("/",response_model=Product,status_code=status.HTTP_201_CREATED)
def create_product(data:ProductCreate,session:Session=Depends(get_session)):
    product=Product(**data.model_dump())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.patch("/{product_id}",response_model=Product)
def update_product(product_id:int,data:ProductUpdate,session:Session=Depends(get_session)):
    product=session.get(Product,product_id)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    product.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:int,session:Session=Depends(get_session)):
    product=session.get(Product,product_id)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    session.delete(product)
    session.commit()