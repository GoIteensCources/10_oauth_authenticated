from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from db import fake_users_db
from werkzeug.security import check_password_hash

route = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# login
@route.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Username or Password incorrect")

    if not check_password_hash(user["hashed_password"], form_data.password):
        raise HTTPException(status_code=400, detail="Username or Password incorrect")

    return {"access_token": user["username"], "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = token
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


