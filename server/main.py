"""
Framework FastAPI using UI Swagger OpenAPI
Interactive API /localhost/docs
Alternative API /localhost/redoc

run application
    uvicorn main:app --port 8500 --host 0.0.0.0 --reload
"""
import secrets
from functools import lru_cache
from routers import secure, callback, intents, card, rule_based
from routers.secure import get_current_active, User
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from internal import Settings
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    openapi_url='/mango/openapi.json',
    redoc_url='/mango/redoc/',
    docs_url='/mango/docs'
)
app.mount('/static', StaticFiles(directory='static'), name='static')

security = HTTPBasic()

origins = [
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://www.mangoconsultant.net",
    'https://mangoserverbot.herokuapp.com'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def get_settings():
    return Settings()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, 'mango')
    correct_password = secrets.compare_digest(credentials.password, 'mango!@#$')
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get('/')
async def homepage():
    return "Welcome to the Server BOT!"


@app.get('/info', tags=['Info'])
async def info(current_user: User = Depends(get_current_active),
               settings: Settings = Depends(get_settings)):
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user,
        'current_user': current_user
    }


app.include_router(
    secure.router,
    prefix='/secure',
    tags=['Secure'],
    responses={418: {'description': "I'm teapot"}},
)

app.include_router(
    callback.router,
    prefix='/callback',
    tags=['Callback'],
    responses={418: {'description': "I'm teapot"}},
)

app.include_router(
    intents.router,
    prefix='/intents',
    tags=['Intents'],
    responses={418: {'description': "I'm teapot"}},
)

app.include_router(
    card.router,
    prefix='/card',
    tags=['Flex Message'],
    responses={418: {'description': "I'm teapot"}},
)

app.include_router(
    rule_based.router,
    prefix='/keyword',
    tags=['Rule Based'],
    responses={418: {'description': "I'm teapot"}},
)

description = """
SERVER BOT APP API helps you do awesome stuff. 🚀

## APIs

You can **read items each API**.

You will be able to:


***OpenAPI Public only prefix /api**
"""


def custom_openapi():
    """
    docs description API
    :return:
        -> func
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Mango-Server BOT",
        version="2.1.0",
        description=description,
        routes=app.routes,
    )
    openapi_schema['info']['x-logo'] = {
        'url': 'https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png'
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
