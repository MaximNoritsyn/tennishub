from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Request

from app.models.cookie import get_context
from app.models.testing_itf import get_test_events

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def index(request: Request = {}):
    context = get_context(request)
    if context.get('logged'):
        context['events'] = get_test_events(context.get('user').person.id_db)

    return templates.TemplateResponse("index.html", context)


