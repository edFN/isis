from __future__ import annotations

from datetime import datetime, timezone, timedelta

import jwt
from fastapi import Depends

from app.device_feature.domain import Device, AccessTokenPayload, DeviceTokenRefresh
from app.device_feature.repository import get_device_repository, get_refresh_repository

SECRET_KEY="SOME_KEY_ONE_TWO"
def create_jwt_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

class DeviceService:
    def __init__(self, device_repository=Depends(get_device_repository),
                 refresh_repository=Depends(get_refresh_repository)):
        self.device_repository = device_repository
        self.refresh_repository = refresh_repository

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

    async def get_device_by_access_token(self, access_token, ip_addr: str):
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])

            if payload['ip_address'] != ip_addr:
                raise ValueError(f"Wrong Ip {ip_addr} ")

            print(payload)

            device = await self.device_repository.find_by_id(payload['device_id'])

            if not device:
                raise ValueError(f"Device not found device_id: {payload['device_id']} ")

            return device

        except Exception as e:
            print(e)

            raise ValueError("Access token not valid")

    async def authenticate_device(self, device_id, private_key, ip_addr: str):
        device = await self.get_by_private_key(private_key)

        if device.device_id != device_id:
            raise ValueError

        payload = AccessTokenPayload(device_id=device_id, ip_address=ip_addr)

        access_token = create_jwt_token(payload.model_dump(), timedelta(minutes=5))
        refresh_token = create_jwt_token(payload.model_dump(), timedelta(days=20))

        refresh_token: DeviceTokenRefresh = DeviceTokenRefresh(
            device_id = device.device_id,
            ip_address = ip_addr,
            refresh_token = refresh_token
        )

        self.refresh_repository.save(refresh_token)

        return access_token, refresh_token.refresh_token

    async def rotate_token(self, refresh_token, ip_addr: str):
        try:

            refresh_token_instance: DeviceTokenRefresh = self.refresh_repository.find_by_key(refresh_token)

            if refresh_token_instance.ip_address != ip_addr:
                raise ValueError("Wrong Ip")

            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            access_payload = AccessTokenPayload(device_id=payload['device_id'],
                                                ip_address=payload['ip_address'])

            access_token = create_jwt_token(access_payload.model_dump(), timedelta(minutes=5))
            refresh_token = create_jwt_token(access_payload.model_dump(), timedelta(days=20))

            self.refresh_repository.delete_token(refresh_token_instance.refresh_token)


            refresh_token: DeviceTokenRefresh = DeviceTokenRefresh(
                device_id=refresh_token_instance.device_id,
                ip_address=refresh_token_instance.ip_address,
                refresh_token=refresh_token
            )

            self.refresh_repository.save(refresh_token)

            return access_token, refresh_token.refresh_token

        except Exception as e:
            print(e)
            raise ValueError("Токен не валидный")







