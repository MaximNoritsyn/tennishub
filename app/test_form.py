from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from typing import Optional
from datetime import date

from app.models.testing_itf import TestEvent, ServingBall, get_name_serving
from app.models.person import Person
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/new/{guid}")
async def new_test(guid: str, request: Request = {}):
    context = get_context(request)
    person = Person.from_db(guid)
    context['name_player'] = person.name
    context['sex'] = person.sex
    context['date_b'] = person.date_b
    context['today'] = date.today()
    return templates.TemplateResponse("new_testing.html", context)


@router.post("/new/{guid}")
async def post_new(request: Request,
                    guid: str,
                    assessor: str = Form(),
                    date: str = Form(),
                    venue: str = Form()):
    test_event = TestEvent()
    test_event.person = Person.from_db(guid)
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
    task = 'gsd'

    context['test_event'] = TestEvent.from_db(guid)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/new'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}'
    context['forbackhand'] = get_detail_serving(stage_number, task)
    context['number'] = stage_number

    name_serving = get_name_serving(task, stage_number)
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
    task = 'gsd'
    name_serving = get_name_serving(task, stage_number)

    setattr(test_event, name_serving, get_point_depth(first_bounce, second_bounce))
    test_event.update()
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.first_bounce = first_bounce
    serving_ball.second_bounce = second_bounce
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/{task}/{stage_number + 1}'
    if stage_number == 10:
        next_route = f'/testing/{guid}/vd/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/vd/{stage_number}")
async def get_test_event_stage_vd(guid: str, stage_number: int, request: Request):
    context = get_context(request)
    task = 'vd'

    context['test_event'] = TestEvent.from_db(guid)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/{guid}/gsd/10'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}'
    context['forbackhand'] = get_detail_serving(stage_number, task)
    context['number'] = stage_number

    name_serving = get_name_serving(task, stage_number)
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
    task = 'vd'
    name_serving = get_name_serving(task, stage_number)

    setattr(test_event, name_serving, get_point_depth(first_bounce, second_bounce))
    test_event.update()
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.first_bounce = first_bounce
    serving_ball.second_bounce = second_bounce
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/{task}/{stage_number + 1}'
    if stage_number == 8:
        next_route = f'/testing/{guid}/gsa/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/gsa/{stage_number}")
async def get_test_event_stage_sda(guid: str, stage_number: int, request: Request):
    context = get_context(request)
    task = 'gsa'

    context['test_event'] = TestEvent.from_db(guid)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/{guid}/vd/8'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}'
    context['forbackhand'] = get_detail_serving(stage_number, task)
    context['number'] = stage_number

    name_serving = get_name_serving(task, stage_number)
    serving_ball = ServingBall.from_db(guid, name_serving)

    context['first_bounce'] = serving_ball.first_bounce
    context['second_bounce'] = serving_ball.second_bounce

    context['title_of_task'] = 'Оцінка точності удару з землі - включає аспект сили. ' \
                               '(6 поперемінних ударів форхендом і бекхендом по лінії та ' \
                               'на кроскорті).'

    return templates.TemplateResponse("test_accuracy.html", context)


@router.post("/{guid}/gsa/{stage_number}")
async def post_test_event_stage_gsa(guid: str,
                                    stage_number: int,
                                    first_bounce: str = Form(default=''),
                                    second_bounce: str = Form(default='')):
    test_event = TestEvent.from_db(guid)
    task = 'gsa'
    name_serving = get_name_serving(task, stage_number)

    setattr(test_event, name_serving, get_point_accuracy(first_bounce, second_bounce))
    test_event.update()
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.first_bounce = first_bounce
    serving_ball.second_bounce = second_bounce
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/{task}/{stage_number + 1}'
    if stage_number == 12:
        next_route = f'/testing/{guid}/serve/1/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/serve/{stage_number}/{serve}")
async def get_test_event_stage_serve(guid: str, stage_number: int, serve: int, request: Request):
    context = get_context(request)
    task = 'serve'

    context['test_event'] = TestEvent.from_db(guid)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}/1'
    if serve == 2:
        context['route_back'] = f'/testing/{guid}/{task}/{stage_number}/1'
    elif stage_number == 1:
        context['route_back'] = f'/testing/{guid}/gsa/12'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}/{serve}'
    context['forbackhand'] = get_detail_serving(stage_number, task, serve)
    context['number'] = stage_number
    context['serve'] = serve

    name_serving = get_name_serving(task, stage_number)
    serving_ball = ServingBall.from_db(guid, name_serving, serve)

    context['first_bounce'] = serving_ball.first_bounce
    context['second_bounce'] = serving_ball.second_bounce

    return templates.TemplateResponse("test_serve.html", context)


@router.post("/{guid}/serve/{stage_number}/{serve}")
async def post_test_event_stage_serve(guid: str,
                                      stage_number: int,
                                      serve: int,
                                      first_bounce: str = Form(default=''),
                                      second_bounce: str = Form(default='')):
    test_event = TestEvent.from_db(guid)
    task = 'serve'
    name_serving = get_name_serving(task, stage_number)

    point = get_point_serve(first_bounce, second_bounce, stage_number, serve)

    setattr(test_event, name_serving, point)
    test_event.update()
    test_event.save()

    next_route = f'/testing/{guid}/{task}/{stage_number + 1}/1'
    if point == 0 and serve == 1:
        next_route = f'/testing/{guid}/{task}/{stage_number}/2'
        second_bounce = ''

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving, serve)
    serving_ball.first_bounce = first_bounce
    serving_ball.second_bounce = second_bounce
    serving_ball.serve = serve
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")

    if stage_number == 12:
        next_route = f'/testing/{guid}/mobility'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/mobility")
async def get_test_event_stage_mobility(guid: str, request: Request):
    context = get_context(request)
    task = 'mobility'

    context['route_back'] = f'/testing/{guid}/serve/12/1'
    context['route_submit'] = f'/testing/{guid}/{task}'

    serving_ball = ServingBall.from_db(guid, 'value_mobility')

    context['first_bounce'] = serving_ball.first_bounce

    return templates.TemplateResponse("test_mobility.html", context)


@router.post("/{guid}/mobility")
async def post_test_event_stage_mobility(guid: str, first_bounce: str = Form(default='')):
    test_event = TestEvent.from_db(guid)
    name_serving = 'value_mobility'

    setattr(test_event, name_serving, get_point_mobility(first_bounce))
    setattr(test_event, 'time_mobility', int(first_bounce))
    test_event.update()
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, 'value_mobility')
    serving_ball.first_bounce = first_bounce
    serving_ball.save()

    response = Response(content=f"mobility submitted")
    response.headers["location"] = f'/testing/{guid}/results'
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/results")
async def get_test_event_stage_results(guid: str, request: Request):
    test_event = TestEvent.from_db(guid)

    context = get_context(request)

    context['test_event'] = test_event
    context['route_back'] = f'/testing/{guid}/mobility'

    return templates.TemplateResponse("test_results.html", context)


def get_detail_serving(stage_number: int, task: str, serve: int = 0):
    res = 'Форхенд'
    if stage_number % 2 == 0:
        res = 'Бекхенд'

    if task == 'gsa':
        suf = 'по лінії'
        if stage_number > 6:
            suf = 'по кроскорту'
        res = f'{res} / {suf}'

    if task == 'serve':
        res = f'{serve} подача'

    return res


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
    if first_bounce == 'area_center_service' or first_bounce == 'area_central_center':
        p = 1
    elif first_bounce == 'area_left_service' or first_bounce == 'area_right_service':
        p = 2
    elif first_bounce == 'area_central_left' or first_bounce == 'area_central_right':
        p = 3

    if p > 0:
        if second_bounce == 'area_out_line':
            p += 1
        elif second_bounce == 'area_out_powerline':
            p *= 2

    return p


def get_point_serve(first_bounce, second_bounce, stage_number, serve):
    p = 0
    if stage_number < 4 and serve == 1:
        if first_bounce == 'area_right_middle_service': p = 2
        if first_bounce == 'area_right_wide_service': p = 4
    elif stage_number < 4 and serve == 2:
        if first_bounce == 'area_right_middle_service': p = 1
        if first_bounce == 'area_right_wide_service': p = 2
    elif stage_number < 7 and serve == 1:
        if first_bounce == 'area_right_wide_service': p = 2
        if first_bounce == 'area_right_middle_service': p = 4
    elif stage_number < 7 and serve == 2:
        if first_bounce == 'area_right_wide_service': p = 1
        if first_bounce == 'area_right_middle_service': p = 2
    elif stage_number < 10 and serve == 1:
        if first_bounce == 'area_left_wide_service': p = 2
        if first_bounce == 'area_left_middle_service': p = 4
    elif stage_number < 10 and serve == 2:
        if first_bounce == 'area_left_wide_service': p = 1
        if first_bounce == 'area_left_middle_service': p = 2
    elif stage_number < 13 and serve == 1:
        if first_bounce == 'area_left_middle_service': p = 2
        if first_bounce == 'area_left_wide_service': p = 4
    elif stage_number < 13 and serve == 2:
        if first_bounce == 'area_left_middle_service': p = 1
        if first_bounce == 'area_left_wide_service': p = 2

    if p > 0:
        if second_bounce == 'area_out_line':
            p += 1
        elif second_bounce == 'area_out_powerline':
            p *= 2

    return p


def get_point_mobility(first_bounce: str):
    data = {
        '40': 1,
        '39': 2,
        '38': 3,
        '37': 4,
        '36': 5,
        '35': 6,
        '34': 7,
        '33': 8,
        '32': 9,
        '31': 10,
        '30': 11,
        '29': 12,
        '28': 12,
        '27': 14,
        '26': 15,
        '25': 16,
        '24': 18,
        '23': 19,
        '22': 21,
        '21': 26,
        '20': 32,
        '19': 39,
        '18': 45,
        '17': 52,
        '16': 61,
        '15': 76
    }

    return data[first_bounce]
