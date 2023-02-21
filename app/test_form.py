from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from typing import Optional
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
    response.headers["location"] = f"/testing/{test_event.id_db}/gsd/1"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/gsd/{stage_number}")
async def get_test_event_stage(guid: str, stage_number: int, request: Request):
    # Your code to retrieve test event and stage information based on the GUID and stage number goes here
    # if guid == test_event.id_db:
    # inplement get new event

    context = get_context(request)

    context['route_back'] = f'/testing/{guid}/gsd/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/new'
    context['route_submit'] = f'/testing/{guid}/gsd/{stage_number}'
    context['forbackhand'] = get_forbackhand(stage_number)
    context['number'] = stage_number

    return templates.TemplateResponse("groundstroke_depth.html", context)


@router.post("/{guid}/gsd/{stage_number}")
async def post_test_event_stage(guid: str,
                                stage_number: int,
                                main_point: Optional[str] = Form(...),
                                sub_point: Optional[str] = Form(...)):
    print(test_event.id_db)
    print(test_event.person.name)

    test_event['value_gsd{:02d}'.format(stage_number)] = get_point_gsd(main_point, sub_point)
    test_event.save()

    response = Response(content=f"stage {stage_number} submitted")
    response.headers["location"] = f'/testing/{guid}/gsd/{stage_number + 1}'
    response.status_code = status.HTTP_302_FOUND
    return response


def get_forbackhand(stage_number):
    if stage_number % 2 == 0:
        return 'Бекхенд'
    else:
        return 'Форхенд'


def get_point_gsd(main_point, sub_point):
    p = 0
    if main_point == 'area_1point_right' or main_point == 'area_1point_left':
        p = 1
    elif main_point == 'area_2point':
        p = 2
    elif main_point == 'area_3point':
        p = 3
    elif main_point == 'area_4point':
        p = 4

    if sub_point == 'area_power_1point':
        p += 1
    elif sub_point == 'area_power_double':
        p *= 2

    return p
