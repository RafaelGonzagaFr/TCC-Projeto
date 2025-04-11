from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import User, Video
from backend.schemas import Message, UserList, UserPublic, UserSchema, VideoList, VideoPublic, VideoSchema
from backend.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/', response_model=VideoPublic)
def create_video(video: VideoSchema, user: T_CurrentUser, session: T_Session, file: UploadFile = File(...)):
    ...#Pegar arquivo, postar na aws Bucket, manipular tabela de vídeo, inserir Título, url(provindo da aws), descrição cravar user atual
  
@router.get('/', response_model=VideoList)
def get_video_by_current_user(user: T_CurrentUser, session: T_Session):
    query = select(Video).where(Video.user_id == user.id)
    ...#Lógica