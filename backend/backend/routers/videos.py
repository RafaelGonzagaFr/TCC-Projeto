from http import HTTPStatus
import os
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from google.cloud import storage

from backend.database import get_session
from backend.models import User, Video
from backend.schemas import Message, UserList, UserPublic, UserSchema, VideoList, VideoPublic, VideoSchema
from backend.security import get_current_user, get_password_hash

router = APIRouter(prefix='/videos', tags=['videos'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

# Caminho para sua chave do Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_key.json"

storage_client = storage.Client() #
bucket = storage_client.bucket("seu-nome-do-bucket")

@router.post('/', response_model=VideoPublic)
async def upload_video(video: VideoSchema, user: T_CurrentUser, session: T_Session, file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Arquivo precisa ser um vídeo.")
    
    # Nome único pro vídeo
    ext = file.filename.split(".")[-1]
    blob_name = f"{user.id}/{uuid4()}.{ext}"

    blob = bucket.blob(blob_name)
    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()

    video = Video(
        title=video.title,
        email=video.descricao,
        url=blob.public_url,
        id=user.id
    )

    session.add(video)
    session.commit()
    session.refresh(video)

    #AJEITAR ESQUEMA COM GOOGLE CLOUD

    return {"video_url": blob.public_url}
  
@router.get('/', response_model=VideoList)
def get_video_by_current_user(user: T_CurrentUser, session: T_Session):
    query = select(Video).where(Video.user_id == user.id)
    ...#Lógica