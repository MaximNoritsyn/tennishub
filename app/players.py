from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Request
from typing import Optional
from datetime import date
from pydantic import EmailStr

from app.models.cookie import get_context
from app.models.person import Person
from app.models.coach_ref import CoachRef
from app.models.testing_itf import get_test_events_by_person

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/new")
def new_person(request: Request = {}):
    context = get_context(request)

    return templates.TemplateResponse("new_player.html", context)


@router.post("/new")
async def create_new_person(request: Request, first_name: str = Form(),
                            last_name: str = Form(),
                            email: Optional[EmailStr] = Form(None),
                            tel: Optional[str] = Form(None),
                            birthday: Optional[date] = Form(None),
                            sex: Optional[str] = Form(None)):

    if getattr(request.state, "logged", False):
        cur_person = Person(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            tel=tel,
                            birthday=birthday,
                            sex=sex)
        cur_person.save()

        coach_ref = CoachRef(cur_person, getattr(request.state, "user", None))
        coach_ref.save()

    response = Response(content="Create new person")
    response.headers["location"] = "/"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}")
def person(guid: str, request: Request = {}):
    context = get_context(request)
    cur_person = Person.from_db(guid)
    if cur_person:
        context['player_name'] = cur_person.first_name + " " + cur_person.last_name
        context['player_guid'] = cur_person.id_db
    context['events'] = get_test_events_by_person(guid)

    return templates.TemplateResponse("list_of_test.html", context)
