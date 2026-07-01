from app.schemas.cart import CartItemResponse, CartResponse, CartItemAdd, CartItemUpdate
from fastapi import APIRouter, Depends
from app.dependencies import get_db, get_current_user
from uuid import UUID
from app.services import cart as cart_service


router = APIRouter(
    prefix="/cart",
    tags=["cart"])


@router.get("/", response_model=CartResponse)
async def get_cart(db=Depends(get_db), user=Depends(get_current_user)):
    return await cart_service.get_cart_details(db, user.id)


@router.post("/items", response_model=CartItemResponse)
async def add_item(payload: CartItemAdd,
    db=Depends(get_db), user=Depends(get_current_user)):
    prod, item = await cart_service.add_item_to_cart(db, user.id, payload)
    return CartItemResponse(
        id = item.product_id,
        product_id = payload.product_id,
        name = prod.name,
        quantity = payload.quantity,
        sell_price = round(prod.sell_price, 2),
        line_total = round(prod.sell_price * payload.quantity, 2),
    )


@router.delete("/item/{prod_id}")
async def delete_item(prod_id: UUID, db=Depends(get_db), user=Depends(get_current_user)):
    await cart_service.delete_item_from_cart(db, user.id, prod_id)
    return {"Deleted" : prod_id}


@router.post("/item/{prod_id}", response_model=CartItemResponse)
async def update_item(prod_id: UUID, payload: CartItemUpdate, db=Depends(get_db), user=Depends(get_current_user)):
    prod, cart_item = await cart_service.update_item_from_cart(
        db,
        user.id,
        prod_id,
        payload
    )
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
    await cart_service.clear_cart(db, user.id)
    return {"Detail" : "Cart cleared"}