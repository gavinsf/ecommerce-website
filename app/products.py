from fastapi import APIRouter, Depends
from app.dependencies import get_db
from app.models import Product
from app.schemas import ProductCreate
from uuid import UUID

router = APIRouter(
    prefix="/products",
    tags=["products"])




# TODO : Require admin
@router.get("/{id}")
async def get_product(id: UUID, db=Depends(get_db)):
    product = await db.get(Product, id)

    if not product:
        return {"error" : "Product not found"}
    
    if product.is_deleted == 1:
        return {"log" : "Product already deleted"}
    
    return product


# TODO : Require admin
@router.post("/")
async def create_product(prod: ProductCreate, db=Depends(get_db)):
    product = Product(**prod.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# TODO : Require admin
@router.delete("/{id}")
async def delete_product(id: UUID, db=Depends(get_db)):
    product = await db.get(Product, id)

    if not product:
        return {"error" : "Product not found"}
    
    product.is_deleted = 1

    await db.commit()

    return {"log" : f"soft deleted {id}"}