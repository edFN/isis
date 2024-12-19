from typing import Optional

from pydantic import BaseModel



class WrongDeviceID(Exception):
    def __init__(self, device_id):
        self.device_id = device_id

    def __str__(self):
        return f'Идентификартор {self.device_id} не является продукцией нашей фирмы!'





class AccessTokenPayload(BaseModel):
    device_id: str
    ip_address: str

class Device(BaseModel):
    device_id: str
    is_blocked: bool = False
    is_active: bool = False

    private_key: Optional[str] = None

    def check_device_id(self):
        if "pi" not in self.device_id:
            raise WrongDeviceID(self.device_id)

    def validate_key(self, key):
        return key == self.private_key


class DeviceTokenRefresh(BaseModel):
    device_id: str = None
    ip_address: str
    refresh_token: str
