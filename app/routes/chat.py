from fastapi import APIRouter, HTTPException

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.deepseek_service import (
    consultar_deepseek
)


router = APIRouter(
    prefix="/api",
    tags=["Chatbot"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    try:

        respuesta = await consultar_deepseek(
            request.message
        )

        return ChatResponse(
            response=respuesta
        )

    except Exception as error:

        print("ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail="No se pudo procesar la consulta."
        )