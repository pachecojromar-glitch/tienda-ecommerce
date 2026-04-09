from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session,select
from db import get_session
from models import User
from auth import login
from schemas.user import UserCreate,UserLogin,UserUpdate

router=APIRouter(prefix="/users",tags=["users"])

@router.get("/",response_model=list[User])
def get_users(session:Session=Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/{user_id}",response_model=User)
def get_user(user_id:int,session:Session=Depends(get_session)):
    user=session.get(User,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate,session:Session=Depends(get_session)):
    new_user=User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.patch("/{user_id}",response_model=User)
def update_user(user_id:int,data:UserUpdate,session:Session=Depends(get_session)):
    user=session.get(User,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    user.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int,session:Session=Depends(get_session)):
    user=session.get(User,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    session.delete(user)
    session.commit()

@router.post("/login")
def user_login(data:UserLogin,session:Session=Depends(get_session)):
    return login(data.email,data.password,session)