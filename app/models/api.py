from fastapi import Query
from fastapi.routing import APIRouter
from app.models.person import Person, get_persons_by_part_of_name

router = APIRouter()


@router.get("/persons")
async def get_persons(search: str = Query(default=None)):
    if search:
        filtered_persons = get_persons_by_part_of_name(search)
        return filtered_persons
    else:
        return []
