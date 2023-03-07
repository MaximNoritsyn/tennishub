import json

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Query, Request
from fastapi.routing import APIRouter

from app.models.person import get_persons_by_part_of_name
from app.models.coach_ref import get_persons_by_coach
from app.models.coach_testing import GroupTest, get_coach_test_by_group
from app.models.testing_itf import TestEvent


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


router = APIRouter()


@router.get("/persons")
async def get_persons(search: str = Query(default=None), username: str = Query(default=None)):
    if search:
        filtered_persons = get_persons_by_part_of_name(search)
        return filtered_persons
    else:
        return get_persons_by_coach(username)


@router.get("/coach_tests")
async def get_persons(group_test_id: str = Query(default=None)):
    if group_test_id:
        group_test = GroupTest.from_db(group_test_id)
        coach_tests = get_coach_test_by_group(group_test)

        return coach_tests
    else:
        return []
