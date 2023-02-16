from fastapi import Response, status, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from app.models.mongobackend import MongoDBBackend
from app.models.access_token import create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/")
async def signup(username: str = Form(), password: str = Form()):
    backend = MongoDBBackend()
    if not backend.add_user(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(username)
    response = Response(content="Logged in")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.headers["location"] = "/"
    response.set_cookie(key="logged", value="1")
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/")
async def signup():
    return templates.TemplateResponse("signup.html", {"request": {}})
