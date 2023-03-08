from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from typing import Optional, List
from datetime import date

import app.models.testing_itf as itf
import app.models.coach_testing as ct
from app.models.testing_itf import TestEvent, ServingBall
from app.models.coach_testing import CoachTest, GroupTest
from app.models.cookie import get_context
from app.models.coach_ref import get_persons_by_coach

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def list_pull_tests(request: Request = {}):
    context = get_context(request)

    context['group_tests'] = ct.get_group_tests_by_coach_username(context.get('user'))

    return templates.TemplateResponse("coach_test_list.html", context)


@router.get("/new")
async def new_tests(request: Request = {}):
    context = get_context(request)
    context['edit'] = True
    context['assessor'] = context.get('user').person.name
    context['today'] = date.today()
    context['group_test_id'] = ''

    return templates.TemplateResponse("coach_test_dashboard.html", context)


@router.post("/new")
async def post_new(request: Request,
                   assessor: str = Form(),
                   v_date: str = Form(),
                   venue: str = Form(),
                   players: Optional[str] = Form()):
    group_test = GroupTest(request.state.user, assessor, date, venue)
    return edit_group_test(group_test, assessor, v_date, venue, players)


@router.post("/{guid}/edit")
async def post_edit(request: Request,
                    guid: str,
                    assessor: str = Form(),
                    v_date: str = Form(),
                    venue: str = Form(),
                    players: Optional[str] = Form()):
    group_test = GroupTest.from_db(guid)
    return edit_group_test(group_test, assessor, v_date, venue, players)


@router.get("/{guid}/dashboard")
async def new_tests(guid: str, request: Request = {}):
    group_test = GroupTest.from_db(guid)
    context = get_context(request)
    context['edit'] = False
    context['group_test'] = group_test
    context['group_test_id'] = guid

    return templates.TemplateResponse("coach_test_dashboard.html", context)


@router.get("/{guid}/gsd/{stage_number}")
async def get_test_event_stage_gsd(guid: str, stage_number: int, request: Request):
    task = 'gsd'

    context = itf.prepare_context_get_court(task, guid, stage_number, request)

    context['route_back'] = f'/coachtesting/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        coach_test = CoachTest.get_by_event(context['test_event'], context.get('user'))
        context['route_back'] = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    context['route_submit'] = f'/coachtesting/{guid}/{task}/{stage_number}'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/gsd/{stage_number}")
async def post_test_event_stage_gsd(guid: str,
                                    stage_number: int,
                                    first_bounce: str = Form(default=''),
                                    second_bounce: str = Form(default='')):
    task = 'gsd'
    test_event = itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce)

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/coachtesting/{guid}/{task}/{stage_number + 1}'
    if stage_number == 10:
        coach_test = CoachTest.get_by_event(test_event)
        coach_test.finish_gsd = True
        coach_test.save()
        next_route = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/vd/{stage_number}")
async def get_test_event_stage_vd(guid: str, stage_number: int, request: Request):
    task = 'vd'

    context = itf.prepare_context_get_court(task, guid, stage_number, request)

    context['route_back'] = f'/coachtesting/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        coach_test = CoachTest.get_by_event(context['test_event'], context.get('user'))
        context['route_back'] = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    context['route_submit'] = f'/coachtesting/{guid}/{task}/{stage_number}'

    return templates.TemplateResponse("test_depth.html", context)


@router.post("/{guid}/vd/{stage_number}")
async def post_test_event_stage_vd(guid: str,
                                   stage_number: int,
                                   first_bounce: str = Form(default=''),
                                   second_bounce: str = Form(default='')):
    task = 'vd'
    test_event = itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce)

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/coachtesting/{guid}/{task}/{stage_number + 1}'
    if stage_number == 8:
        coach_test = CoachTest.get_by_event(test_event)
        coach_test.finish_vd = True
        coach_test.save()
        next_route = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/gsa/{stage_number}")
async def get_test_event_stage_sda(guid: str, stage_number: int, request: Request):
    task = 'gsa'

    context = itf.prepare_context_get_court(task, guid, stage_number, request)

    context['route_back'] = f'/coachtesting/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        coach_test = CoachTest.get_by_event(context['test_event'], context.get('user'))
        context['route_back'] = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    context['route_submit'] = f'/coachtesting/{guid}/{task}/{stage_number}'

    return templates.TemplateResponse("test_accuracy.html", context)


@router.post("/{guid}/gsa/{stage_number}")
async def post_test_event_stage_gsa(guid: str,
                                    stage_number: int,
                                    first_bounce: str = Form(default=''),
                                    second_bounce: str = Form(default='')):
    task = 'gsa'
    test_event = itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce)

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/coachtesting/{guid}/{task}/{stage_number + 1}'
    if stage_number == 12:
        coach_test = CoachTest.get_by_event(test_event)
        coach_test.finish_gsa = True
        coach_test.save()
        next_route = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/serve/{stage_number}/{serve}")
async def get_test_event_stage_serve(guid: str, stage_number: int, serve: int, request: Request):
    task = 'serve'

    context = itf.prepare_context_get_court(task, guid, stage_number, request, serve)

    context['route_back'] = f'/coachtesting/{guid}/{task}/{stage_number - 1}/1'
    if serve == 2:
        context['route_back'] = f'/coachtesting/{guid}/{task}/{stage_number}/1'
    elif stage_number == 1:
        coach_test = CoachTest.get_by_event(context['test_event'], context.get('user'))
        context['route_back'] = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    context['route_submit'] = f'/coachtesting/{guid}/{task}/{stage_number}/{serve}'

    return templates.TemplateResponse("test_serve.html", context)


@router.post("/{guid}/serve/{stage_number}/{serve}")
async def post_test_event_stage_serve(guid: str,
                                      stage_number: int,
                                      serve: int,
                                      first_bounce: str = Form(default=''),
                                      second_bounce: str = Form(default='')):
    task = 'serve'
    test_event = itf.save_results_serve_test(task, guid, stage_number, first_bounce, second_bounce, serve)

    point = itf.get_point_serve(first_bounce, second_bounce, stage_number, serve)

    next_route = f'/coachtesting/{guid}/{task}/{stage_number + 1}/1'
    if point == 0 and serve == 1:
        next_route = f'/coachtesting/{guid}/{task}/{stage_number}/2'

    response = Response(content=f"stage {stage_number} submitted")

    if stage_number == 12:
        coach_test = CoachTest.get_by_event(test_event)
        coach_test.finish_serve = True
        coach_test.save()
        next_route = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    response.headers["location"] = next_route
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/mobility")
async def get_test_event_stage_mobility(guid: str, request: Request):
    context = get_context(request)
    task = 'mobility'

    test_event = TestEvent.from_db(guid)
    coach_test = CoachTest.get_by_event(test_event)

    context['route_back'] = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    context['route_submit'] = f'/coachtesting/{guid}/{task}'

    serving_ball = ServingBall.from_db(guid, 'value_mobility')

    context['first_bounce'] = serving_ball.first_bounce

    return templates.TemplateResponse("test_mobility.html", context)


@router.post("/{guid}/mobility")
async def post_test_event_stage_mobility(guid: str, first_bounce: str = Form(default='')):
    test_event = itf.save_results_mobility(guid, first_bounce)

    coach_test = CoachTest.get_by_event(test_event)
    coach_test.finish_mobility = True
    coach_test.save()

    response = Response(content=f"mobility submitted")
    response.headers["location"] = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    response.status_code = status.HTTP_302_FOUND
    return response


def edit_group_test(group_test: GroupTest,
                    assessor: str = Form(),
                    v_date: str = Form(),
                    venue: str = Form(),
                    players: Optional[str] = Form()):
    group_test.date = v_date
    group_test.assessor = assessor
    group_test.venue = venue
    group_test.save()
    if players:
        persons_ids_list = players.split(',')
        for person_id in persons_ids_list:
            CoachTest.get_by_person(person_id, group_test)
    response = Response(content="Create group of test")
    response.headers["location"] = f"/coachtesting/{group_test.id_db}/dashboard"
    response.status_code = status.HTTP_302_FOUND
    return response