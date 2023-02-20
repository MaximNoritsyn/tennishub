from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from app.models.users import verify_password
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/")
async def login(username: str = Form(), password: str = Form()):
    access_token = verify_password(username, password)
    response = Response(content="Logged in")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.headers["location"] = "/"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/")
async def login_form(request: Request = {}):
    context = get_context(request)
    return templates.TemplateResponse("login.html", context)

