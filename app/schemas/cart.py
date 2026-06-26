import uuid
from pydantic import BaseModel, Field

class CartItemAdd(BaseModel):
    product_id     : uuid.UUID
    quantity       : int = Field(gt=0, default=1)

class CartItemResponse(BaseModel):
    product_id     : uuid.UUID
    quantity       : int
    price          : float
    name           : str

class CartResponse(BaseModel):
    items : list[CartItemResponse]
    total : float

class CartItemUpdate(BaseModel):
    quantity       : int = Field(gt=0, default=1)