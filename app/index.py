from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Request

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def index(request: Request = {}):
    print("test")
    logged = False
    username = ""
    if not Request == {}:
        if hasattr(request.state, "username"):
            username = request.state.username
        if hasattr(request.state, "logged"):
            logged = request.state.logged
    return templates.TemplateResponse("index.html", {"request": request, "logged": logged, "username": username})


