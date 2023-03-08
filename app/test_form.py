from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from typing import Optional
from datetime import date

import app.models.testing_itf as itf
from app.models.testing_itf import TestEvent, ServingBall
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
    task = 'gsd'

    context = itf.prepare_context_get_court(task, guid, stage_number, request)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/new'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/gsd/{stage_number}")
async def post_test_event_stage_gsd(guid: str,
                                    stage_number: int,
                                    first_bounce: str = Form(default=''),
                                    second_bounce: str = Form(default='')):
    task = 'gsd'
    itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce)

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/{task}/{stage_number + 1}'
    if stage_number == 10:
        next_route = f'/testing/{guid}/vd/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/vd/{stage_number}")
async def get_test_event_stage_vd(guid: str, stage_number: int, request: Request):
    task = 'vd'

    context = itf.prepare_context_get_court(task, guid, stage_number, request)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/{guid}/gsd/10'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/vd/{stage_number}")
async def post_test_event_stage_vd(guid: str,
                                   stage_number: int,
                                   first_bounce: str = Form(default=''),
                                   second_bounce: str = Form(default='')):
    task = 'vd'
    itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce)

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/{task}/{stage_number + 1}'
    if stage_number == 8:
        next_route = f'/testing/{guid}/gsa/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/gsa/{stage_number}")
async def get_test_event_stage_sda(guid: str, stage_number: int, request: Request):
    task = 'gsa'

    context = itf.prepare_context_get_court(task, guid, stage_number, request)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        context['route_back'] = f'/testing/{guid}/vd/8'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}'

    return templates.TemplateResponse("test_accuracy.html", context)


@router.post("/{guid}/gsa/{stage_number}")
async def post_test_event_stage_gsa(guid: str,
                                    stage_number: int,
                                    first_bounce: str = Form(default=''),
                                    second_bounce: str = Form(default='')):
    task = 'gsa'
    itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce)

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/testing/{guid}/{task}/{stage_number + 1}'
    if stage_number == 12:
        next_route = f'/testing/{guid}/serve/1/1'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/serve/{stage_number}/{serve}")
async def get_test_event_stage_serve(guid: str, stage_number: int, serve: int, request: Request):
    task = 'serve'

    context = itf.prepare_context_get_court(task, guid, stage_number, request, serve)

    context['route_back'] = f'/testing/{guid}/{task}/{stage_number - 1}/1'
    if serve == 2:
        context['route_back'] = f'/testing/{guid}/{task}/{stage_number}/1'
    elif stage_number == 1:
        context['route_back'] = f'/testing/{guid}/gsa/12'
    context['route_submit'] = f'/testing/{guid}/{task}/{stage_number}/{serve}'

    return templates.TemplateResponse("test_serve.html", context)


@router.post("/{guid}/serve/{stage_number}/{serve}")
async def post_test_event_stage_serve(guid: str,
                                      stage_number: int,
                                      serve: int,
                                      first_bounce: str = Form(default=''),
                                      second_bounce: str = Form(default='')):
    task = 'serve'
    itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce, serve)

    point = itf.get_point_serve(first_bounce, second_bounce, stage_number, serve)

    next_route = f'/testing/{guid}/{task}/{stage_number + 1}/1'
    if point == 0 and serve == 1:
        next_route = f'/testing/{guid}/{task}/{stage_number}/2'

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
    itf.save_results_mobility(guid, first_bounce)

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

