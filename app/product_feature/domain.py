from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):

    id: Optional[int] = None

    name: str = "Неизвестно"
    produced_at: datetime = datetime.now()
    expire_at: Optional[datetime] = None

    device_id: str

    def is_expired(self):

        if self.expire_at is None:
            return False

        return datetime.now() >= self.expire_at

class ProductCreate(BaseModel):
    name: str = "Неизвестно"
    produced_at: datetime = datetime.now()
    expire_at: Optional[datetime] = None