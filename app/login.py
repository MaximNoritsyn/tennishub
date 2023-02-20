from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
import bcrypt

from app.models.users import User
from app.models.cookie import get_context, create_access_token

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


def verify_password(username: str, password: str) -> str:
    user, hashed_password = User.from_db(username)
    verified = False
    if user is not None:
        verified = bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    return create_access_token(user)
