from pydantic import BaseModel, ConfigDict
import uuid
import datetime

class OrderCreateResponse(BaseModel):
    order_id        : uuid.UUID
    total           : float
    created_at      : datetime.datetime
