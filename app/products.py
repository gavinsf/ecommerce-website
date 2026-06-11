from fastapi import APIRouter, Depends
from app.dependencies import get_db
from app.models import Product
from app.schemas import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["products"])


# TODO : Require admin
@router.post("/")
async def create_product(prod: ProductCreate, db=Depends(get_db)):
    db_product = Product(**prod.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product