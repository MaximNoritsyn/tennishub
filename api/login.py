from fastapi import Response, status
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("")
async def login(username: str, password: str, response: Response):
    # Your authentication logic here
    if username == "admin" and password == "secret":
        response.status_code = status.HTTP_302_FOUND
        response.headers["Location"] = "/dashboard"
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@router.get("")
async def login_form():
    return templates.TemplateResponse("login.html", {"request": {}})
