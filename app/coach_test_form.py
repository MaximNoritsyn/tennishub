from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from typing import Optional
from datetime import date

import app.models.testing_itf as itf
import app.models.coach_testing as ct
from app.models.testing_itf import TestEvent, ServingBall
from app.models.coach_testing import CoachTest, GroupTest
from app.models.cookie import get_context

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

    return templates.TemplateResponse("coach_test_dashboard.html", context)


@router.post("/new")
async def post_new(request: Request,
                    assessor: str = Form(),
                    date: str = Form(),
                    venue: str = Form()):
    group_test = GroupTest(request.state.user, assessor, date, venue)
    group_test.save()
    response = Response(content="Create group of test")
    response.headers["location"] = f"/coachtesting/{group_test.id_db}/dashboard"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/edit")
async def new_tests(guid: str, request: Request = {}):
    group_test = GroupTest.from_db(guid)
    context = get_context(request)
    context['group_test'] = group_test
    context['edit'] = True
    context['assessor'] = group_test.assessor
    context['today'] = group_test.date
    context['today'] = group_test.date

    return templates.TemplateResponse("coach_test_dashboard.html", context)


@router.post("/{guid}/edit")
async def post_edit(request: Request,
                    guid: str,
                    assessor: str = Form(),
                    date: str = Form(),
                    venue: str = Form()):
    group_test = GroupTest.from_db(guid)
    group_test.date = date
    group_test.assessor = assessor
    group_test.venue = venue
    group_test.save()
    response = Response(content="Create group of test")
    response.headers["location"] = f"/coachtesting/{group_test.id_db}/dashboard"
    response.status_code = status.HTTP_302_FOUND
    return response


@router.get("/{guid}/dashboard")
async def new_tests(guid: str, request: Request = {}):
    group_test = GroupTest.from_db(guid)
    context = get_context(request)
    context['edit'] = False
    context['group_test'] = group_test

    return templates.TemplateResponse("coach_test_dashboard.html", context)
