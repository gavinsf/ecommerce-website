from fastapi import APIRouter, Depends, Query
from app.dependencies import get_db, require_admin
from app.models import Product
from app.schemas import ProductCreate
from uuid import UUID
from sqlalchemy import select

router = APIRouter(
    prefix="/products",
    tags=["products"])


# TODO : Require admin
@router.get("/")
async def list_products(offset: int = Query(0, ge=0),
    limit: int = Query(20, le=50),
    db=Depends(get_db)):
    result = await db.execute(
        select(Product).offset(offset).limit(limit)
    )
    
    products = result.scalars().all()    

    if not products:
        return {"Error" : "Products not found"}

    return products


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
@router.post("/", dependencies=[Depends(require_admin)])
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