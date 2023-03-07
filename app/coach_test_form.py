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
                   persons: Optional[str] = Form()):
    group_test = GroupTest(request.state.user, assessor, date, venue)
    return edit_group_test(group_test, assessor, v_date, venue, persons)


@router.post("/{guid}/edit")
async def post_edit(request: Request,
                    guid: str,
                    assessor: str = Form(),
                    v_date: str = Form(),
                    venue: str = Form(),
                    persons: Optional[str] = Form()):
    group_test = GroupTest.from_db(guid)
    return edit_group_test(group_test, assessor, v_date, venue, persons)


@router.get("/{guid}/dashboard")
async def new_tests(guid: str, request: Request = {}):
    group_test = GroupTest.from_db(guid)
    context = get_context(request)
    context['edit'] = False
    context['group_test'] = group_test
    context['group_test_id'] = guid

    return templates.TemplateResponse("coach_test_dashboard.html", context)


def edit_group_test(group_test: GroupTest,
                    assessor: str = Form(),
                    v_date: str = Form(),
                    venue: str = Form(),
                    persons: Optional[str] = Form()):
    group_test.date = v_date
    group_test.assessor = assessor
    group_test.venue = venue
    group_test.save()
    if persons:
        persons_ids_list = persons.split(',')
        for person_id in persons_ids_list:
            CoachTest.get_by_person(person_id, group_test)
    response = Response(content="Create group of test")
    response.headers["location"] = f"/coachtesting/{group_test.id_db}/dashboard"
    response.status_code = status.HTTP_302_FOUND
    return response
