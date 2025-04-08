from pydantic import BaseModel, ConfigDict, EmailStr

from backend.models import Tipo


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    tipo: Tipo


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]

class VideoSchema(BaseModel):
    title: str
    descricao: str
    url: str

class VideoPublic(VideoSchema):
    id: int

class VideoList(BaseModel):
    videos: list[VideoPublic]