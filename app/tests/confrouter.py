import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

from app.main import app
from app.database import Base, get_db

from dotenv import load_dotenv
import os

TEST_DB_URL = os.getenv("DB")
ALEMBIC_URL = os.getenv("ALEMBIC_DB")

@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", ALEMBIC_URL)
    command.upgrade(alembic_cfg, "head")
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    connection = await db_engine.connect()
    trans = await connection.begin()

    async_session_factory = sessionmaker(
        connection,
        class_=async_session_factory,
        expire_on_commit=False
    )
    session = async_session_factory()

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()