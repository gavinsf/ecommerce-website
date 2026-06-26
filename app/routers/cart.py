from app.schemas.cart import CartItemResponse, CartResponse, CartItemAdd, CartItemUpdate
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db, get_current_user
from app.models import Product, CartItem
from sqlalchemy import select

router = APIRouter(
    prefix="/cart",
    tags=["cart"])

@router.post("/items", response_model=CartItemResponse)
async def add_item_cart(payload: CartItemAdd,
    db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(Product).where(Product.id == payload.product_id)
    res = await db.execute(sel)
    prod = res.scalars().first()

    if not prod:
        raise HTTPException(status_code=404, detail="Product cannot be found")
    
    if prod.is_deleted == 1:
        raise HTTPException(status_code=403, detail="Product is deleted")
    
    sel = select(CartItem).where(
        CartItem.user_id == user.id,
        CartItem.product_id == payload.product_id
    )
    res = await db.execute(sel)
    existing = res.scalars().first()

    if existing:
        existing.quantity += payload.quantity
        item = existing
    else:
        item = CartItem(id = user.id, product_id = payload.product_id, quantity = payload.quantity)
        db.add(item)
    await db.commit()
    await db.refresh(item)

    return CartItemResponse(
        product_id = payload.id,
        quantity = payload.quantity,
        price = round(prod.sell_price * payload.quantity, 2),
        name = prod.name
    )

@router.delete("/item/{id}")
async def delete_item_cart(id, db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(CartItem).where(
        CartItem.product_id==id,
        CartItem.user_id==user
    )
    res = await db.execute(sel)
    item = res.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(item)
    db.commit()
    return {"Deleted" : id}

@router.post("/item/{id}", response_model=CartItemResponse)
async def update_item_cart(id, payload=CartItemUpdate, db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(CartItem, Product).join(Product).where(
        CartItem.product_id==id,
        CartItem.user_id==user
    )
    res = await db.execute(sel)
    row = res.scalars().first()

    if not row:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    item, prod = row
    item.quantity = payload.quantity

    await db.commit()

    return CartItemResponse(
        product_id = payload.id,
        quantity = payload.quantity,
        price = round(prod.sell_price * payload.quantity, 2),
        name = prod.name
    )