from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.engine import engine


LocalSession = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Get async session for FastAPI Depends."""
    async with LocalSession() as session:
        yield session
