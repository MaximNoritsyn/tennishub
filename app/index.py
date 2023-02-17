from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Request
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def index(request: Request = {}):
    context = get_context(request)
    return templates.TemplateResponse("index.html", context)


