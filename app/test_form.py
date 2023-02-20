from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from datetime import date

from app.models.testing_itf import TestEvent
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

TestEvent = TestEvent()


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
    TestEvent.person = request.state.user.person
    TestEvent.assessor = assessor
    TestEvent.date = date
    TestEvent.venue = venue
    TestEvent.save()
