from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates/")


@router.get("/", response_class=HTMLResponse)
def index(request: Request, name: str = None, message: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "name": name, "message": message})
