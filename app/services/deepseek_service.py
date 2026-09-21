import json
from pathlib import Path

import httpx

from app.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)

from app.services.core_service import (
    obtener_productos,
    obtener_espacios,
    obtener_movimientos,
    obtener_resumen,
)


BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.txt"


def cargar_prompt():
    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as archivo:
        return archivo.read()


async def consultar_deepseek(message: str):

    if not DEEPSEEK_API_KEY:
        raise Exception(
            "No se encontró DEEPSEEK_API_KEY en el archivo .env"
        )

    # 1. Cargar prompt del sistema
    system_prompt = cargar_prompt()

    # 2. Consultar datos reales desde el Core de SmartLuben
    productos = await obtener_productos()
    espacios = await obtener_espacios()
    movimientos = await obtener_movimientos()
    resumen = await obtener_resumen()

    # 3. Agrupar datos del Core
    datos = {
        "productos": productos,
        "espacios": espacios,
        "movimientos": movimientos,
        "resumen": resumen,
    }

    # 4. Convertir datos a JSON para enviarlos como contexto
    contexto = json.dumps(
        datos,
        ensure_ascii=False,
        indent=2,
        default=str
    )

    # 5. Construir el contexto completo para DeepSeek
    mensaje_sistema = f"""
{system_prompt}

DATOS ACTUALES DEL SISTEMA SMARTLUBEN:

{contexto}
"""

    # 6. Preparar payload para DeepSeek
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": mensaje_sistema
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    # 7. Cabeceras de autenticación
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # 8. Preparar URL de DeepSeek
    base_url = DEEPSEEK_BASE_URL.strip().rstrip("/")

    if not base_url.startswith(("http://", "https://")):
        base_url = f"https://{base_url}"

    url = f"{base_url}/chat/completions"

    print("URL DeepSeek:", url)

    # 9. Enviar consulta a DeepSeek
    async with httpx.AsyncClient(timeout=30.0) as client:

        response = await client.post(
            url,
            json=payload,
            headers=headers
        )

        response.raise_for_status()

        data = response.json()

        # 10. Devolver respuesta generada
        respuesta = data["choices"][0]["message"]["content"]
        respuesta = (
            respuesta
            .replace("**", "")
            .replace("```", "")
        )

        return respuesta.strip()