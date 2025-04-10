import token

from fastapi import FastAPI

from backend.routers import token, users

app = FastAPI()
app.include_router(users.router)
app.include_router(token.router)
