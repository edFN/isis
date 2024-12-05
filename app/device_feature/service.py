from datetime import datetime

from fastapi import Depends

from app.device_feature.domain import Device
from app.device_feature.repository import get_device_repository


class DeviceService:
    def __init__(self, device_repository=Depends(get_device_repository)):
        self.device_repository = device_repository

    async def register_device(self, device_id: str):

        device = Device(device_id=device_id)

        device.check_device_id()

        device.private_key = f"SOME_KEY{datetime.now().timestamp()}"

        device.is_active = True

        return await self.device_repository.save(device)

    async def get_device(self, device_id):
        return self.device_repository.get(device_id)

    async def get_by_private_key(self, private_key):
        return await self.device_repository.find_by_key(private_key)
