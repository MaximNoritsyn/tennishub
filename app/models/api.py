from fastapi import Query,Request
from fastapi.routing import APIRouter
from app.models.person import Person, get_persons_by_part_of_name
from app.models.coach_ref import get_persons_by_coach

router = APIRouter()


@router.get("/persons")
async def get_persons(search: str = Query(default=None), username: str = Query(default=None)):
    if search:
        filtered_persons = get_persons_by_part_of_name(search)
        return filtered_persons
    else:
        return get_persons_by_coach(username)
