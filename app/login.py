from fastapi import Response, status, HTTPException, Form, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
import configparser
import jwt

from app.models.mongobackend import MongoDBBackend

router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['ACCESS_TOKEN']['SECRET_KEY']
ALGORITHM = config['ACCESS_TOKEN']['ALGORITHM']


def create_access_token(username: str) -> str:
    to_encode = {"sub": username}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    backend = MongoDBBackend()
    if not backend.verify_password(credentials.username, credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(credentials.username)
    response = Response(content="Logged in")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.headers["location"] = "/dashboard"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/")
async def login_form():
    return templates.TemplateResponse("login.html", {"request": {}})


@router.get("/dashboard")
async def dashboard():
    return templates.TemplateResponse("index.html", {})