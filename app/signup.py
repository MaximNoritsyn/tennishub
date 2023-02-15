from fastapi import Response, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
import configparser
import jwt

from app.models.users import User
from app.models.mongobackend import MongoDBBackend

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/", response_model=User)
async def signup(user):
    pass
    # user = User(**user.dict())
    # print(user)
    # return user


@router.get("/")
async def signup():
    return templates.TemplateResponse("signup.html", {"request": {}})
