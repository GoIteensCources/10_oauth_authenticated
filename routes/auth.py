from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials, HTTPBearer
from fastapi_sso import GoogleSSO
from starlette import status

from db import fake_users_db
from werkzeug.security import check_password_hash
from settings import settings_app as s

route = APIRouter()

security = HTTPBearer()

db = {}

def get_google_sso() -> GoogleSSO:
    return GoogleSSO(s.GOOGLE_CLIENT_ID,
                     s.GOOGLE_CLIENT_SECRET,
                     redirect_uri=f"http://{s.HOST}:{s.PORT}/auth/google/callback")


@route.get("/google/login")
async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
    return await google_sso.get_login_redirect()


@route.get("/google/callback")
async def google_callback(request: Request, google_sso: GoogleSSO = Depends(get_google_sso)):
    user = await google_sso.verify_and_process(request)
    db[user.id] = user
    return user


@route.get("/getdb")
async def get_db(request: Request):
    return db


async def get_current_user(token: HTTPBasicCredentials = Depends(security)):
    print(token)
    user = db.get(token.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
# login
# @route.post("/token")
# async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = fake_users_db.get(form_data.username)
#     if not user:
#         raise HTTPException(status_code=400, detail="Username or Password incorrect")
#
#     if not check_password_hash(user["hashed_password"], form_data.password):
#         raise HTTPException(status_code=400, detail="Username or Password incorrect")
#
#     return {"access_token": user["username"], "token_type": "bearer"}


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     username = token
#     user = fake_users_db.get(username)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Невірний токен",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_admin(current_user=Depends(get_current_user)):
#     if not current_user["is_admin"]:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail="only for admin",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return current_user
