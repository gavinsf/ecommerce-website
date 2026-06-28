from app.schemas.cart import CartItemResponse, CartResponse, CartItemAdd, CartItemUpdate
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db, get_current_user
from app.models import Product, CartItem
from sqlalchemy import select
from uuid import UUID

router = APIRouter(
    prefix="/cart",
    tags=["cart"])

@router.get("/", response_model=CartResponse)
async def get_cart(db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(CartItem, Product).join(Product).where(
        CartItem.user_id == user.id
    )
    res = await db.execute(sel)
    rows = res.all()

    items = []
    for ci, prod in rows:
        items.append(CartItemResponse(
            id=ci.id, product_id=prod.id, quantity=ci.quantity,
            sell_price=prod.sell_price, name=prod.name,
            line_total=round(prod.sell_price*ci.quantity, 2)
        ))
    total = round(sum(i.line_total for i in items), 2)
    return CartResponse(items=items, total=total)

@router.post("/items", response_model=CartItemResponse)
async def add_item(payload: CartItemAdd,
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
        item = CartItem(
            user_id = user.id,
            product_id = payload.product_id,
            quantity = payload.quantity,
            )
        db.add(item)
    await db.commit()
    await db.refresh(item)

    return CartItemResponse(
        id = item.id,
        product_id = payload.product_id,
        name = prod.name,
        quantity = payload.quantity,
        sell_price = round(prod.sell_price, 2),
        line_total = round(prod.sell_price * payload.quantity, 2),
    )

@router.delete("/item/{prod_id}")
async def delete_item(prod_id: UUID, db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(CartItem).where(
        CartItem.product_id==prod_id,
        CartItem.user_id==user.id
    )
    res = await db.execute(sel)
    item = res.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    await db.delete(item)
    await db.commit()
    return {"Deleted" : prod_id}

@router.post("/item/{prod_id}", response_model=CartItemResponse)
async def update_item(prod_id: UUID, payload: CartItemUpdate, db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(CartItem, Product).join(Product).where(
        CartItem.product_id==prod_id,
        CartItem.user_id==user.id
    )
    res = await db.execute(sel)
    row = res.first()

    if not row:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart_item, prod = row
    cart_item.quantity = payload.quantity

    await db.commit()

    return CartItemResponse(
        id = cart_item.id,
        product_id = prod_id,
        quantity = payload.quantity,
        sell_price = round(prod.sell_price, 2),
        name = prod.name,
        line_total = round(prod.sell_price * payload.quantity, 2),
    )

@router.delete("/")
async def clear_cart(db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(CartItem).where(CartItem.user_id==user.id)
    res = await db.execute(sel)
    items = res.scalars().all()

    if not items:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    for item in items:
        await db.delete(item)
    await db.commit()

    return {"Detail" : "Cart cleared"}