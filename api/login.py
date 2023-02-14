from fastapi import Response, status, Cookie, Header
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/")
async def login(username: str, password: str, response: Response, secure: bool = Header(None)):
    # Your authentication logic here
    if username == "admin" and password == "secret":
        response.status_code = status.HTTP_302_FOUND
        response.headers["Location"] = "/dashboard"
        response.set_cookie(key="session_token", value="session_value", secure=secure)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@router.get("/")
async def login_form(session_token: str = Cookie(None)):
    if session_token is None:
        return templates.TemplateResponse("login.html", {"request": {}})
    return templates.TemplateResponse("index.html", {"request": {}})
