# sim_post_cap_backend/app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings # Import the settings

async_engine = create_async_engine(
    str(settings.ASYNC_SQLALCHEMY_DATABASE_URI), # Use the assembled async URI
    echo=settings.DEBUG_MODE, # Control echo with DEBUG_MODE
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session