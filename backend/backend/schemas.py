from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    matricula: str
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
