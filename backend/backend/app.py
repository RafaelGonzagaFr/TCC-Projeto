from fastapi import FastAPI

from backend.schemas import UserPublic, UserSchema

app = FastAPI()


@app.post('/users', response_model=UserPublic)
def create_user(user: UserSchema):
    return user
