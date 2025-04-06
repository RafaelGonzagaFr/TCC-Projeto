import csv
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.security import get_current_user, get_password_hash
from backend.database import get_session
from backend.models import User
from backend.schemas import Message, UserList, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
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

    hashed_password = get_password_hash(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        matricula=user.matricula,
        password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    current_user: T_CurrentUser,
    session: Session = Depends(get_session),
    limit: int = 10,
    skip: int = 0,
):
    if current_user.tipo == 'adm':
        user = session.scalars(select(User).limit(limit).offset(skip))
        return {'users': user}
    else:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )


@router.post('/csv', status_code=HTTPStatus.OK, response_model=Message)
async def create_users_by_csv_file(current_user: T_CurrentUser, session: T_Session, file: UploadFile = File(...)):
    if current_user.tipo == 'adm':
            if file.filename.endswith('.csv'):
                contents = await file.read()

                with open(file.filename, 'wb') as f:
                    f.write(contents)

                with open(file.filename, newline='') as csvfile:
                    users = csv.DictReader(csvfile)
                    for user_in_csv in users:
                        db_user = session.scalar(
                            select(User).where(
                                (User.matricula == user_in_csv['matricula']) | (User.email == user_in_csv['email'])
                            )
                        )

                        if db_user:
                            break

                        hashed_password = user_in_csv['password']

                        if user_in_csv['tipo'].lower() == 'aluno':
                            db_user = User(
                                name=user_in_csv['username'],
                                email=user_in_csv['email'],
                                password=hashed_password,
                                matricula=user_in_csv['matricula'],
                                tipo='aluno'
                            )
                        elif user_in_csv['tipo'].lower() == 'professor':
                            db_user = User(
                                name=user_in_csv['username'],
                                email=user_in_csv['email'],
                                password=hashed_password,
                                matricula=user_in_csv['matricula'],
                                tipo='aluno'
                            )
                        else:
                            break

                        session.add(db_user)
                        session.commit()
                        session.refresh(db_user)

            return {'message': 'Adição feita'}
    else:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):

    if current_user.tipo != 'adm':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.email = user.email
    current_user.name = user.username
    current_user.password = get_password_hash(user.password)
    current_user.matricula = user.matricula

    session.commit()
    session.refresh(current_user)

    return current_user
