import json
from pathlib import Path

import httpx

from app.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)


BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.txt"
DATA_PATH = BASE_DIR / "data" / "mock_data.json"


def cargar_prompt():
    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as archivo:
        return archivo.read()


def cargar_datos():
    with open(
        DATA_PATH,
        "r",
        encoding="utf-8"
    ) as archivo:
        return json.load(archivo)


async def consultar_deepseek(message: str):

    if not DEEPSEEK_API_KEY:
        raise Exception(
            "No se encontró DEEPSEEK_API_KEY en el archivo .env"
        )

    system_prompt = cargar_prompt()
    datos = cargar_datos()

    contexto = json.dumps(
        datos,
        ensure_ascii=False,
        indent=2
    )

    mensaje_sistema = f"""
{system_prompt}

DATOS ACTUALES DE SMARTLUBEN:

{contexto}
"""

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

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    base_url = DEEPSEEK_BASE_URL.strip().rstrip("/")
    if not base_url.startswith(("http://", "https://")):
        base_url = f"https://{base_url}"

    url = f"{base_url}/chat/completions"

    print("URL DeepSeek:", url)

    async with httpx.AsyncClient(timeout=30.0) as client:

        response = await client.post(
            url,
            json=payload,
            headers=headers
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]