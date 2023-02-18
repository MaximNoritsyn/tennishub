from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from app.models.mongobackend import MongoDBBackend
from app.models.cookie import create_access_token
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/")
async def signup(username: str = Form(), password: str = Form()):
    backend = MongoDBBackend()
    if not backend.add_user(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(username)
    response = Response(content="Logged in")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.headers["location"] = "/"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/")
async def signup(request: Request = {}):
    context = get_context(request)
    return templates.TemplateResponse("signup.html", context)
