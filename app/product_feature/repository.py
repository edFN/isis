from app.product_feature.domain import Product


FAKE_PRODUCT_DB = [
    Product(name="Молоко", device_id="pi211",)
]

class ProductRepository:
    async def save(self, product: Product):
        ...

    async def get_all(self, device_id):
        ...

class InMemoryProductRepository(ProductRepository):
    async def save(self, product: Product):
        product.id = len(FAKE_PRODUCT_DB) + 1
        FAKE_PRODUCT_DB.append(product)
        return product

    async def get_all(self, device_id: str):
        found = []

        for product in FAKE_PRODUCT_DB:
            if product.device_id == device_id:
                found.append(product)

        return found


def get_product_repository():
    return InMemoryProductRepository()