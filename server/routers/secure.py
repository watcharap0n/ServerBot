import os
import pytz
from typing import Optional
from firebase_admin import auth, exceptions
from internal import db, Id
from config.firebase_auth import ConfigFirebase
from config import firebaseConfig, firebaseAuth
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from starlette.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status, Depends, Form, File, UploadFile, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
EXPIRES_TOKEN = 60 * 60 * 1
EXPIRES_REMEMBER = 60 * 60 * 24 * 5

collection = 'secure'

router = APIRouter()
config = ConfigFirebase(path_auth=firebaseAuth, path_db=firebaseConfig)
pb = config.authentication()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/secure/login")


def verify_password(plain_password, hashed_password):
    """

    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """

    :param password:
    :return:
    """
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """

    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        refresh = auth.verify_session_cookie(token, check_revoked=True)
        auth.revoke_refresh_tokens(refresh['sub'])
        return refresh
    except auth.RevokedSessionCookieError:
        return credentials_exception
    except auth.InvalidSessionCookieError:
        raise credentials_exception


async def authentication_cookie(form_data: OAuth2PasswordRequestForm = Depends()):
    """

    :param form_data:
    :return:
    """
    sign_user = pb.sign_in_with_email_and_password(form_data.username, form_data.password)
    check_verify = auth.get_user_by_email(form_data.username)
    if not check_verify.email_verified:
        pb.send_email_verification(sign_user.get('idToken'))
        return HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail={'status': True, 'message': 'email verification!',
                    '_data': check_verify._data}
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail={'status': True, 'message': 'login success!',
                '_data': check_verify._data},
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        content = jsonable_encoder(credentials_exception)
        session_cookie = auth.create_session_cookie(id_token=sign_user.get('idToken'), expires_in=timedelta(hours=1))
        response = JSONResponse(content=content)
        response.set_cookie(key='session', value=str(session_cookie),
                            expires=EXPIRES_TOKEN)
        return {"access_token": session_cookie, "token_type": "bearer"}
    except exceptions.FirebaseError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Failed to create a session cookie')


def payload_register(**val):
    """

    :param val:
    :return:
    """
    return val


@router.get('/user')
async def read_users_me(current_user=Depends(get_current_user)):
    """

    :param current_user:
    :return:
    """
    return current_user


@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login(user=Depends(authentication_cookie)):
    """

    :param user:
    :return:
    """
    return user


@router.post('/register')
async def register(
        file: Optional[UploadFile] = File(None),
        email: str = Form(...),
        hashed_password: str = Form(...),
        username: str = Form(...),
        full_name: str = Form(...),
        disabled: bool = Form(True),
):
    """

    :param file:
    :param email:
    :param hashed_password:
    :param username:
    :param full_name:
    :param disabled:
    :return:
    """
    try:
        http = str()
        if file:
            filename = file.filename
            upload_dir = os.path.join('static', 'uploads')
            file_input = os.path.join(upload_dir, file.filename)
            http += f'https://mangoserverbot.herokuapp.com/static/uploads/profiles/{filename}'
            with open(file_input, 'wb+') as upload_file:
                upload_file.write(file.file.read())
                upload_file.close()
        user = auth.create_user(
            email=email,
            password=hashed_password,
            display_name=username,
            photo_url=None if not http else http,
        )
        tz = pytz.timezone('Asia/Bangkok')
        _d = datetime.now(tz)
        date = _d.strftime('%d/%m/%y')
        time = _d.strftime('%H:%M:%S')
        data = payload_register(
            username=username,
            email=email,
            hashed_password=get_password_hash(hashed_password),
            full_name=full_name,
            img_path=http,
            date=date,
            time=time,
            disabled=disabled,
            _data=user.__dict__.get('_data')
        )
        db.insert_one('secure', data)
        return user.__dict__
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='your register already exists')


@router.get('/encoding')
async def encoding(token: str = Depends(oauth2_scheme)):
    """

    :param token:
    :return:
    """
    return {'status': True, 'message': 'encoding session', 'session': token}


@router.get('/refresh')
async def socket_auth(request: Request):
    """

    :param request:
    :return:
    """
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='session cookie is null'
        )
    try:
        refresh = auth.verify_session_cookie(session_cookie, check_revoked=True)
        auth.revoke_refresh_tokens(refresh['sub'])
        return refresh
    except auth.InvalidSessionCookieError:
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        raise exception