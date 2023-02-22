from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from typing import Optional
from datetime import date

from app.models.testing_itf import TestEvent, ServingBall
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


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
    test_event = TestEvent()
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
async def get_test_event_stage_gsd(guid: str, stage_number: int, request: Request):

    context = get_context(request)

    context['route_back'] = f'/testing/{guid}/gsd/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/new'
    context['route_submit'] = f'/testing/{guid}/gsd/{stage_number}'
    context['forbackhand'] = get_forbackhand(stage_number)
    context['number'] = stage_number

    name_serving = get_name_serving('gsd', stage_number)
    serving_ball = ServingBall.from_db(guid, name_serving)

    context['groundstroke1'] = serving_ball.groundstroke1
    context['groundstroke2'] = serving_ball.groundstroke2

    context['title_of_task'] = 'Оцінка глибини удару по землі - включає аспект потужності. ' \
                               '(10 поперемінних ударів форхендом і бекхендом)'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/gsd/{stage_number}")
async def post_test_event_stage_gsd(guid: str,
                                stage_number: int,
                                groundstroke1: str = Form(default=''),
                                groundstroke2: str = Form(default='')):
    test_event = TestEvent.from_db(guid)
    name_serving = get_name_serving('gsd', stage_number)

    setattr(test_event, name_serving, get_point_gsd(groundstroke1, groundstroke2))
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.groundstroke1 = groundstroke1
    serving_ball.groundstroke2 = groundstroke2
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/gsd/{stage_number + 1}'
    if stage_number == 10:
        next_route = f'/testing/{guid}/vd/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/vd/{stage_number}")
async def get_test_event_stage_vd(guid: str, stage_number: int, request: Request):

    context = get_context(request)

    context['route_back'] = f'/testing/{guid}/vd/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/{guid}/gsd/10'
    context['route_submit'] = f'/testing/{guid}/vd/{stage_number}'
    context['forbackhand'] = get_forbackhand(stage_number)
    context['number'] = stage_number

    name_serving = get_name_serving('vd', stage_number)
    serving_ball = ServingBall.from_db(guid, name_serving)

    context['groundstroke1'] = serving_ball.groundstroke1
    context['groundstroke2'] = serving_ball.groundstroke2

    context['title_of_task'] = 'Оцінка глибини залпу - включає аспект сили. ' \
                               '(8 поперемінних ударів ударами форхендом і бекхендом)'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/vd/{stage_number}")
async def post_test_event_stage_vd(guid: str,
                                stage_number: int,
                                groundstroke1: str = Form(default=''),
                                groundstroke2: str = Form(default='')):
    test_event = TestEvent.from_db(guid)
    name_serving = get_name_serving('vd', stage_number)

    setattr(test_event, name_serving, get_point_gsd(groundstroke1, groundstroke2))
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.groundstroke1 = groundstroke1
    serving_ball.groundstroke2 = groundstroke2
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/vd/{stage_number + 1}'
    if stage_number == 8:
        next_route = f'/testing/{guid}/gsv/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


def get_forbackhand(stage_number):
    if stage_number % 2 == 0:
        return 'Бекхенд'
    else:
        return 'Форхенд'


def get_point_gsd(groundstroke1, groundstroke2):
    p = 0
    if groundstroke1 == 'area_left_service' or groundstroke1 == 'area_right_service':
        p = 1
    elif groundstroke1 == 'area_central1':
        p = 2
    elif groundstroke1 == 'area_central2':
        p = 3
    elif groundstroke1 == 'area_central3':
        p = 4

    if p > 0:
        if groundstroke2 == 'area_power_1point':
            p += 1
        elif groundstroke2 == 'area_power_double':
            p *= 2

    return p


def get_name_serving(task, stage_number):

    if task == 'gsd':
        return 'value_gsd{:02d}'.format(stage_number)
    elif task == 'vd':
        return 'value_vd{:02d}'.format(stage_number)
    elif task == '':
        return 'value_gsa{:02d}'.format(stage_number)
