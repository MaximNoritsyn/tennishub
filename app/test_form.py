from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from datetime import date

from app.models.testing_itf import TestEvent
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

test_event = TestEvent()


@router.get("/new")
async def new_test(request: Request = {}):
    context = get_context(request)
    if context.get('logged'):
        context['sex'] = context.get('user').person.sex
        context['date_b'] = context.get('user').person.date_b
        context['today'] = date.today()
        return templates.TemplateResponse("new_testing.html", context)
    else:
        return templates.TemplateResponse("login.html", context)


@router.post("/new")
async def post_new(request: Request,
                   assessor: str = Form(),
                   date: str = Form(),
                   venue: str = Form()):
    test_event.person = request.state.user.person
    test_event.assessor = assessor
    test_event.date = date
    test_event.venue = venue
    test_event.save()
    response = Response(content="Create new testing ITF")
    response.headers["location"] = f"/testing/{test_event.id_db}/gsd/01"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/gsd/{stage_number}")
async def get_test_event_stage(guid: str, stage_number: int, request: Request):
    # Your code to retrieve test event and stage information based on the GUID and stage number goes here
    # if guid == test_event.id_db:

    context = get_context(request)
    return templates.TemplateResponse("groundstroke_depth.html", context)
