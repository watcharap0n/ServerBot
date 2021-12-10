"""
Framework FastAPI using UI Swagger OpenAPI
Interactive API /localhost/docs
Alternative API /localhost/redoc

run application

uvicorn main:app --port 8500 --host 0.0.0.0
"""
import os
from functools import lru_cache
from routers import users
from fastapi import FastAPI, Depends
from internal import Settings
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@lru_cache()
def get_settings():
    return Settings()


@app.get('/info')
async def info(settings: Settings = Depends(get_settings)):
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user,
    }


app.include_router(
    users.router,
    prefix='/users',
    tags=['Users'],
    responses={418: {'description': "I'm teapot"}}
)


def custom_openapi():
    """
    docs description API
    :return:
        -> func
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Server-Mango AI.CRM",
        version="2.0.0",
        description="This is OpenAPI Public only using prefix path /api",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
