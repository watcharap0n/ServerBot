from internal import db, Id
from models.user import User, UserInDB
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


collection = 'secure'

router = APIRouter()


def hash_password(password: str):
    return "hashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/secure/token")


def get_user(db, username: str):
    for user in db:
        if username == user.get('username'):
            user_dict = user
            return UserInDB(**user_dict)


def decode_token(token):
    users = db.find(collection=collection, query={})
    user = get_user(users, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post('/register')
async def register():
    pass



@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = db.find(collection=collection, query={})
    for user_dict in users:
        if form_data.username == user_dict.get('username'):
            if not user_dict:
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            user = UserInDB(**user_dict)
            hashed_password = hash_password(form_data.password)
            if not hashed_password == user.hashed_password:
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
