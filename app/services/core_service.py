import httpx

from app.config import CORE_API_URL


async def obtener_productos():
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{CORE_API_URL}/productos"
        )
        response.raise_for_status()
        return response.json()


async def obtener_espacios():
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{CORE_API_URL}/espacios"
        )
        response.raise_for_status()
        return response.json()


async def obtener_movimientos():
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{CORE_API_URL}/movimientos"
        )
        response.raise_for_status()
        return response.json()


async def obtener_resumen():
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{CORE_API_URL}/dashboard/resumen"
        )
        response.raise_for_status()
        return response.json()
        