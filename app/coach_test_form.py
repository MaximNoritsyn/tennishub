from fastapi import Response, status, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from typing import Optional
from datetime import date

import app.models.testing_itf as itf
from app.models.testing_itf import TestEvent, ServingBall
from app.models.cookie import get_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def list_pull_tests(request: Request = {}):
    context = get_context(request)

    return templates.TemplateResponse("new_testing.html", context)

