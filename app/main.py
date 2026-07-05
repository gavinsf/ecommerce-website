from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.routers.products import router as products_router
from app.routers.orders import router as orders_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(products_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(orders_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    pass