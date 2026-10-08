from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url)


async def check_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1 + 1"))
        return result.scalar_one()
