from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def index():
    return templates.TemplateResponse("index.html", {"request": {}})
