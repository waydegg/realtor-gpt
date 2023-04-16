from httpx import AsyncClient

from .clients import database


async def get_conn():
    async with database.connection() as conn:
        yield conn


async def get_client():
    async with AsyncClient() as client:
        yield client
