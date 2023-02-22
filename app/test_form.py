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

    context['first_bounce'] = serving_ball.first_bounce
    context['second_bounce'] = serving_ball.second_bounce

    context['title_of_task'] = 'Оцінка глибини удару по землі - включає аспект потужності. ' \
                               '(10 поперемінних ударів форхендом і бекхендом)'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/gsd/{stage_number}")
async def post_test_event_stage_gsd(guid: str,
                                stage_number: int,
                                first_bounce: str = Form(default=''),
                                second_bounce: str = Form(default='')):
    test_event = TestEvent.from_db(guid)
    name_serving = get_name_serving('gsd', stage_number)

    p = get_point_depth(first_bounce, second_bounce)
    stability = get_stability(test_event, 'gsd', stage_number)

    setattr(test_event, name_serving, p + stability)
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.first_bounce = first_bounce
    serving_ball.second_bounce = second_bounce
    serving_ball.stability = stability
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

    context['first_bounce'] = serving_ball.first_bounce
    context['second_bounce'] = serving_ball.second_bounce

    context['title_of_task'] = 'Оцінка глибини залпу - включає аспект сили. ' \
                               '(8 поперемінних ударів ударами форхендом і бекхендом)'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/vd/{stage_number}")
async def post_test_event_stage_vd(guid: str,
                                stage_number: int,
                                first_bounce: str = Form(default=''),
                                second_bounce: str = Form(default='')):
    test_event = TestEvent.from_db(guid)
    name_serving = get_name_serving('vd', stage_number)

    p = get_point_depth(first_bounce, second_bounce)
    stability = get_stability(test_event, 'vd', stage_number)

    setattr(test_event, name_serving, p+stability)
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.first_bounce = first_bounce
    serving_ball.second_bounce = second_bounce
    serving_ball.stability = stability
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/vd/{stage_number + 1}'
    if stage_number == 8:
        next_route = f'/testing/{guid}/gsa/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/gsa/{stage_number}")
async def get_test_event_stage_sda(guid: str, stage_number: int, request: Request):

    context = get_context(request)

    context['route_back'] = f'/testing/{guid}/gsa/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/{guid}/vd/8'
    context['route_submit'] = f'/testing/{guid}/gsa/{stage_number}'
    context['forbackhand'] = get_forbackhand(stage_number)
    context['number'] = stage_number

    name_serving = get_name_serving('gsa', stage_number)
    serving_ball = ServingBall.from_db(guid, name_serving)

    context['first_bounce'] = serving_ball.first_bounce
    context['second_bounce'] = serving_ball.second_bounce

    context['title_of_task'] = 'Оцінка точності удару з землі - включає аспект сили. ' \
                               '(6 поперемінних ударів форхендом і бекхендом по лінії та ' \
                               '6 поперемінних ударів форхендом і бекхендом на кроскорті).'

    return templates.TemplateResponse("test_accuracy.html", context)


def get_forbackhand(stage_number):
    if stage_number % 2 == 0:
        return 'Бекхенд'
    else:
        return 'Форхенд'


def get_point_depth(first_bounce, second_bounce):
    p = 0
    if first_bounce == 'area_left_service' or first_bounce == 'area_right_service':
        p = 1
    elif first_bounce == 'area_central1':
        p = 2
    elif first_bounce == 'area_central2':
        p = 3
    elif first_bounce == 'area_central3':
        p = 4

    if p > 0:
        if second_bounce == 'area_out_line':
            p += 1
        elif second_bounce == 'area_out_powerline':
            p *= 2

    return p


def get_point_accuracy(first_bounce, second_bounce):
    p = 0
    if first_bounce == 'area-center-service-bottom' or first_bounce == 'area-central-center':
        p = 1
    elif first_bounce == 'area-left-service-bottom' or first_bounce == 'area-right-service-bottom':
        p = 2
    elif first_bounce == 'area-central-left' or first_bounce == 'area-central-right':
        p = 3

    if p > 0:
        if second_bounce == 'area_out_line':
            p += 1
        elif second_bounce == 'area_out_powerline':
            p *= 2

    return p


def get_name_serving(task, stage_number):

    if task == 'gsd':
        return 'value_gsd{:02d}'.format(stage_number)
    elif task == 'vd':
        return 'value_vd{:02d}'.format(stage_number)
    elif task == 'gsa':
        return 'value_gsa{:02d}'.format(stage_number)


def get_stability(test_event, task, stage_number):

    prev_res = 0
    """
    if stage_number == 1:
        if task == 'vd':
            prev_res = getattr(test_event, get_name_serving('gsd', 10))
        elif task == 'gsa':
            prev_res = getattr(test_event, get_name_serving('vd', 8))
        
    else:
    """
    if stage_number > 1:
        prev_res = getattr(test_event, get_name_serving(task, stage_number-1))

    return 1 if prev_res > 0 else 0

