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
    context = get_context(request)
    task = 'gsd'

    test_event = TestEvent.from_db(guid)
    context['test_event'] = test_event
    context['gsd'] = True

    context['route_back'] = f'/coachtesting/{guid}/{task}/{stage_number - 1}'
    if stage_number == 1:
        coach_test = CoachTest.get_by_event(test_event, context.get('user'))
        context['route_back'] = f'/coachtesting/{coach_test.group_test.id_db}/dashboard'
    context['route_submit'] = f'/coachtesting/{guid}/{task}/{stage_number}'
    context['forbackhand'] = itf.get_detail_serving(stage_number, task)
    context['number'] = stage_number

    name_serving = itf.get_name_serving(task, stage_number)
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
    name_serving = itf.get_name_serving(task, stage_number)

    setattr(test_event, name_serving, itf.get_point_depth(first_bounce, second_bounce))
    test_event.update()
    test_event.save()

    serving_ball = ServingBall.from_db(test_event.id_db, name_serving)
    serving_ball.first_bounce = first_bounce
    serving_ball.second_bounce = second_bounce
    serving_ball.save()

    response = Response(content=f"stage {stage_number} submitted")
    next_route = f'/coachtesting/{guid}/{task}/{stage_number + 1}'
    if stage_number == 10:
        next_route = f'/coachtesting/dashboard'
    response.headers["location"] = next_route
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