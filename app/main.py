from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.routers.products import router as products_router
from app.routers.orders import router as orders_router

app = FastAPI()

app.include_router(products_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(orders_router, prefix="/api")

@app.get("/")
async def root():
    pass