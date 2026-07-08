import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from alembic.config import Config
from alembic import command
from sqlalchemy import text
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base
from app.dependencies import get_db


from dotenv import load_dotenv
import os

load_dotenv()

TEST_DB_URL = os.getenv("TEST_DB")

def run_migrations_up():
    alembic_cfg = Config("alembic.ini")
    sync_url = TEST_DB_URL.replace("asyncpg", "psycopg2") if "asyncpg" in TEST_DB_URL else TEST_DB_URL
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)
    command.upgrade(alembic_cfg, "head")

def run_migrations_down():
    alembic_cfg = Config("alembic.ini")
    sync_url = TEST_DB_URL.replace("asyncpg", "psycopg2") if "asyncpg" in TEST_DB_URL else TEST_DB_URL
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)
    command.downgrade(alembic_cfg, "base")

@pytest_asyncio.fixture(scope="session")
async def db_engine():
    run_migrations_up()
    
    engine = create_async_engine(TEST_DB_URL, echo=False, poolclass=NullPool)
    
    yield engine
    
    await engine.dispose()
    
    # Tear down migrations at the very end
    run_migrations_down()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    # Use context managers to guarantee clean connection state on the current loop
    async with db_engine.connect() as connection:
        async with connection.begin() as transaction:
            async_session_factory = async_sessionmaker(
                bind=connection,
                class_=AsyncSession,
                expire_on_commit=False
            )
            async with async_session_factory() as session:
                yield session
            
            # Forces a rollback after the test finishes, 
            # even if your app code called `await db.commit()`
            await transaction.rollback()
