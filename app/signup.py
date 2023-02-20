from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from pydantic import EmailStr
from datetime import date
from typing import Optional

from app.models.cookie import create_access_token
from app.models.cookie import get_context
from app.models.users import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/")
async def signup(username: str = Form(),
                 password: str = Form(),
                 name: str = Form(),
                 date_b: Optional[date] = Form(None),
                 sex: Optional[str] = Form(None),
                 email: EmailStr = Form()):
    user = User(username, email, name, date_b=date_b, sex=sex)
    user.save(password=password)
    access_token = create_access_token(user)
    response = Response(content="Logged in")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.headers["location"] = "/"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/")
async def signup(request: Request = {}):
    context = get_context(request)
    return templates.TemplateResponse("signup.html", context)
