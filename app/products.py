from fastapi import APIRouter, Depends
from app.dependencies import get_db
from app.models import Product
from app.schemas import ProductCreate
from uuid import UUID

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


@router.delete("/{id}")
async def delete_product(id: UUID, db=Depends(get_db)):
    product = await db.get(Product, id)

    if not product:
        return {"error" : "Product not found"}
    
    product.is_deleted = True

    await db.commit()

    return {"log" : f"soft deleted {id}"}