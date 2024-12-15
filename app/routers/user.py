try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
    from app.database import crud
except Exception as error:
    raise ("Erro de biblioteca: %s" % error)

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/", response_model=List[UserSchema])
def get_all_users_route(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@router.get("/{user_id}", response_model=UserSchema)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserSchema)
def update_user_route(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, update_data)

@router.put("/{user_id}/password", response_model=UserSchema)
def update_user_password_route(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user_password(db, user_id, update_data)

@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)
