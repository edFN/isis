from abc import abstractmethod

from app.device_feature.domain import Device

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



DEVICE_FAKE_DB = {
    "pi211": Device(device_id="pi211",
                            private_key="some_key",
                            is_active=True),
    "my_pi_bla_bla": Device(device_id="my_pi_bla_bla",
                            private_key="some_key123",
                            is_active=True)
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



def get_device_repository():
    return InMemoryDeviceRepository()