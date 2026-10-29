"""POE Backend — Database base and session factory."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

_engine = None
_session_factory = None


def init_engine(database_url: str):
    global _engine, _session_factory
    _engine = create_async_engine(database_url, echo=False, pool_pre_ping=True)
    _session_factory = sessionmaker(
        _engine, class_=AsyncSession, expire_on_commit=False
    )


async def get_session() -> AsyncSession:
    if _session_factory is None:
        raise RuntimeError("Database engine not initialized. Call init_engine() first.")
    async with _session_factory() as session:
        yield session