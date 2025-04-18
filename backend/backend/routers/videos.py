from http import HTTPStatus
import os
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_key.json" #CHAVE DO GOO GLE CLOUD

storage_client = storage.Client() #
bucket = storage_client.bucket("arandu-bucket-videos") #BUCKET

#ESSA PARTE AQUI É PRA FAZER UPLOAD DO VIDEO

@router.post('/', response_model=VideoPublic)
async def upload_video(user: T_CurrentUser, session: T_Session, title: str = Form(...), descricao: str = Form(...), file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Arquivo precisa ser um vídeo.")
    
    # Nome único pro vídeo
    ext = file.filename.split(".")[-1]
    blob_name = f"{user.id}/{uuid4()}.{ext}"

    blob = bucket.blob(blob_name)
    blob.upload_from_file(file.file, content_type=file.content_type)

    video = Video(
        title=title,
        description=descricao,
        url=blob.public_url,
        user_id=user.id,
        status='analise'
    )

    session.add(video)
    session.commit()
    session.refresh(video)

    #AJEITAR ESQUEMA COM GOOGLE CLOUD

    return video

#TESTAR
@router.get('/feed', response_model=VideoList)
def get_videos_aprovados(session: T_Session):
    videos = session.scalar(
        select(Video).where(
            (Video.status == 'aprovado')
        )
    )
    return videos

##TESTAAAAARR
@router.get('/analise', response_model=VideoList)
def get_videos_analise(user: T_CurrentUser, session: T_Session):
    if user.tipo == 'professor':
        videos = session.scalar(
            select(Video).where(
                (Video.status == 'analise')
            )
        )

        return videos
    else:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

##TESTAAAAARR
@router.put('/aprovar/{video_id}', response_model=Message)
def mudar_status_video(user: T_CurrentUser, session: T_Session, video_id: int):
    if user.tipo == 'professor':
        video = session.scalar(
            select(Video).where(
                (Video.id == video_id)
            )
        )

        video.status = 'aprovado'

        session.commit()
        session.refresh(video)

        return {'Status': 'Aprovado'}

##MUDAR ISSO DAQUI
@router.get("/assistir/{video_id}")
def assistir_video(video_id: int, session: Session = Depends(get_session)):
    video = session.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    return video

##TESTAAAR
@router.get('/usuario', response_model=VideoList)
def get_video_by_current_user(user: T_CurrentUser, session: T_Session):
    videos = session.query(Video).filter(Video.user_id == user.id)
    return videos