import uuid
from pydantic import BaseModel, Field

class CartItemAdd(BaseModel):
    product_id     : uuid.UUID
    quantity       : int = Field(gt=0, default=1)

class CartItemUpdate(BaseModel):
    quantity      : int = Field(gt=0, default=1)

class CartItemResponse(BaseModel):
    id:         uuid.UUID
    product_id: uuid.UUID
    name:       str
    quantity:   int
    sell_price: float
    line_total: float

class CartResponse(BaseModel):
    items : list[CartItemResponse]
    total : float

class CartItemUpdate(BaseModel):
    quantity       : int = Field(gt=0, default=1)