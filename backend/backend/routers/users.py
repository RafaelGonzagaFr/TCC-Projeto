from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import User
from backend.schemas import UserList, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.matricula == user.matricula) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.matricula == user.matricula:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='matricula já existe',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='email já existe',
            )

    db_user = User(
        name=user.name,
        email=user.email,
        matricula=user.matricula,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    session: Session = Depends(get_session),
    limit: int = 10,
    skip: int = 0,
):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': user}
