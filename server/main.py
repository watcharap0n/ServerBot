from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(
    users.router,
    prefix='/users',
    tags=['Users'],
    responses={418: {'description': "I'm teapot"}}
)
