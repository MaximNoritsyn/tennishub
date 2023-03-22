from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Request

from app.models.cookie import get_context
from app.models.testing_itf import get_test_events_by_person
from app.models.coach_ref import get_persons_by_coach

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def index(request: Request = {}):
    context = get_context(request)
    if context.get('logged'):
        user = context.get('user')
        if user.person.is_coach:
            context['players'] = get_persons_by_coach(user.username)
        else:
            context['events'] = get_test_events_by_person(user.person.id_db)
            context['player_guid'] = user.person.id_db

    return templates.TemplateResponse("index.html", context)


