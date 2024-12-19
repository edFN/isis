from abc import abstractmethod, ABC

from app.device_feature.domain import Device, DeviceTokenRefresh


class IDeviceRepository:
    @abstractmethod
    def save(self, device: Device):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, device_id):
        raise NotImplementedError

    @abstractmethod
    async def find_by_key(self, private_key: str):
        raise NotImplementedError

class RefreshTokenRepository:
    def save(self, refresh_device: DeviceTokenRefresh):
        pass

    def find_by_key(self, refresh_token: str):
        pass

    def delete_token(self, refresh_token: str):
        pass




DEVICE_FAKE_DB = {
    "pi211": Device(device_id="pi211",
                            private_key="some_key",
                            is_active=True),
    "my_pi_bla_bla": Device(device_id="my_pi_bla_bla",
                            private_key="some_key123",
                            is_active=True)
}

REFRESH_FAKE_DB = {

}

class InMemoryDeviceRepository(IDeviceRepository):

    async def save(self, device: Device):

        if device.device_id in DEVICE_FAKE_DB:
            raise Exception

        DEVICE_FAKE_DB[device.device_id] = device
        return device

    async def find_by_id(self, device_id):
        if device_id not in DEVICE_FAKE_DB:
            return None

        return DEVICE_FAKE_DB[device_id]

    async def find_by_key(self, private_key):
        for device in DEVICE_FAKE_DB.values():
            if device.private_key == private_key:
                return device

        raise Exception("Ничего не найдено")

class InMemoryRefreshRepository(RefreshTokenRepository):
    def save(self, refresh_device: DeviceTokenRefresh):
        REFRESH_FAKE_DB[refresh_device.refresh_token] = refresh_device
        return refresh_device

    def find_by_key(self, refresh_token):

        if refresh_token in REFRESH_FAKE_DB:
            return REFRESH_FAKE_DB[refresh_token]
        else:
            raise ValueError

    def delete_token(self, refresh_token: str):
        if refresh_token in REFRESH_FAKE_DB:
            del REFRESH_FAKE_DB[refresh_token]



def get_refresh_repository():
    return InMemoryRefreshRepository()

def get_device_repository():
    return InMemoryDeviceRepository()