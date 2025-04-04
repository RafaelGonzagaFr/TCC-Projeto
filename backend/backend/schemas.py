from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    matricula: str
    password: str


class UserPublic(BaseModel):
    id: str
    username: str
    email: EmailStr
