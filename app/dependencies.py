from app.database import SessionLocal

async def get_db():
    # yields an async DB session per request, auto-closes on exit
    async with SessionLocal() as session:
        yield session