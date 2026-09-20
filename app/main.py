from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.routes.chat import router as chat_router


app = FastAPI(
    title="LubenBot API",
    description=(
        "Chatbot inteligente para consultas "
        "del sistema SmartLuben."
    ),
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


app.include_router(chat_router)


@app.get("/")
async def inicio(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "LubenBot"
    }