from fastapi import FastAPI
from app.products import router as products_router

app = FastAPI()

app.include_router(products_router, prefix="/api")

@app.get("/")
async def root():
    pass