from fastapi import APIRouter, Depends, Query
from app.dependencies import get_db, require_admin
from app.schemas.products import ProductCreate
from uuid import UUID
from app.services import products as prod_service

router = APIRouter(
    prefix="/products",
    tags=["products"])


@router.get("/")
async def list_products(offset: int = Query(0, ge=0),
    limit: int = Query(20, le=50), db=Depends(get_db)):
    return await prod_service.list_products(db, offset, limit)


@router.get("/{id}")
async def get_product(id: UUID, db=Depends(get_db)):    
    return await prod_service.get_product(db, id)


@router.post("/", dependencies=[Depends(require_admin)])
async def create_product(prod: ProductCreate, db=Depends(get_db)):
    return await prod_service.create_product(db, prod)


@router.delete("/{id}", dependencies=[Depends(require_admin)])
async def delete_product(id: UUID, db=Depends(get_db)):
    await prod_service.soft_delete_product(db, id)
    return {"log" : f"soft deleted {id}"}