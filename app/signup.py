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
                 first_name: str = Form(),
                 last_name: str = Form(),
                 birthday: Optional[date] = Form(None),
                 sex: Optional[str] = Form(None),
                 tel: Optional[str] = Form(None),
                 is_coach_str: str = Form(),
                 email: Optional[EmailStr] = Form(None)):
    is_coach = False
    if is_coach_str == 'true':
        is_coach = True
    user = User(username,
                first_name=first_name,
                last_name=last_name,
                tel=tel,
                is_coach=is_coach,
                birthday=birthday,
                email=email,
                sex=sex)
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
