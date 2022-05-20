from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import Config
from tgbot.services.db_base import Base
from tgbot.services.utils import make_connection_string


async def create_db_session(config: Config):
    engine = create_async_engine(
        make_connection_string(config),
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session
