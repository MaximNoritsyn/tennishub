from fastapi import FastAPI, Response
from fastapi.templating import Jinja2Templates
from auth import authenticate

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.post("/login")
async def login(username: str, password: str, response: Response):
    await authenticate(username, password, response)


@app.get("/login")
async def login_form():
    return templates.TemplateResponse("login.html", {"request": {}})
