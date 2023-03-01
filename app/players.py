from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Request
from typing import Optional
from datetime import date

from app.models.cookie import get_context
from app.models.person import Person
from app.models.coach_ref import CoachRef
from app.models.testing_itf import get_test_events

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/new")
def new_person(request: Request = {}):
    context = get_context(request)

    return templates.TemplateResponse("new_player.html", context)


@router.post("/new")
async def create_new_person(request: Request, name: str = Form(),
                            date_b: Optional[date] = Form(None),
                            sex: Optional[str] = Form(None)):

    context = get_context(request)
    if getattr(request.state, "logged", False):
        print('save person: ', context.get('Logged'))
        person = Person(name=name, date_b=date_b, sex=sex)
        person.save()

        coach_ref = CoachRef(person, getattr(request.state, "user", None))
        coach_ref.save()

    response = Response(content="Create new person")
    response.headers["location"] = "/"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}")
def person(guid: str, request: Request = {}):
    context = get_context(request)
    cur_person = Person.get_from_db(guid)
    print(cur_person)
    if cur_person:
        context['player_name'] = cur_person.name
    context['events'] = get_test_events(guid)

    return templates.TemplateResponse("list_of_test.html", context)
