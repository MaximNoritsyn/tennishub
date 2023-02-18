from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from app.models.cookie import create_access_token
from app.models.mongobackend import MongoDBBackend
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/new")
async def login_form(request: Request = {}):
    context = get_context(request)
    if context.get('logged'):
        return templates.TemplateResponse("new_testing.html", context)
    else:
        return templates.TemplateResponse("login.html", context)
