from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session,select
from sqlalchemy.orm import selectinload
from db import get_session
from models import Comment
from schemas.comment import CommentCreate,CommentUpdate

router=APIRouter(prefix="/comments",tags=["comments"])

@router.get("/",response_model=list[Comment])
def get_comments(session:Session=Depends(get_session)):
    return session.exec(select(Comment)).all()

@router.get("/{comment_id}",response_model=Comment)
def get_comment(comment_id:int,session:Session=Depends(get_session)):
    comment=session.get(Comment,comment_id)
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    return comment

@router.post("/",response_model=Comment,status_code=status.HTTP_201_CREATED)
def create_comment(comment:CommentCreate,session:Session=Depends(get_session)):
    new_comment=Comment(**comment.model_dump())
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@router.patch("/{comment_id}",response_model=Comment)
def update_comment(comment_id:int,data:CommentUpdate,session:Session=Depends(get_session)):
    comment=session.get(Comment,comment_id)
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    comment.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

@router.delete("/{comment_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id:int,session:Session=Depends(get_session)):
    comment=session.get(Comment,comment_id)
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    session.delete(comment)
    session.commit()