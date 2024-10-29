from fastapi import APIRouter, Depends, Request
from routes import get_current_user

route = APIRouter()


@route.get("/account")
async def get_account(current_user=Depends(get_current_user)):
    return current_user


@route.get("/get_header")
async def get_account(request: Request, current_user=Depends(get_current_user)):
    return request.headers
