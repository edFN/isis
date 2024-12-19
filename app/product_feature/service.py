from random import choice

from fastapi import Depends

from app.product_feature.repository import get_product_repository




class ProductFeatureService:
    def __init__(self, repository = Depends(get_product_repository)):
        self.repository = repository

    def insert(self, product):
        return self.repository.save(product)

    def list(self, device_id: str):
        return self.repository.get_all(device_id)

    async def get_recipe(self, device_id):
        RANDOM_RECIPE = [
            """
            Бутерброды с творожным сыром и овощами. 
            Ингредиенты: 100 г творожного сыра, 2 веточки петрушки, 
            2 зубчика чеснока, 1 авокадо, 1 огурец, 2 помидора, специи, 
            хлеб. 1 Приготовление: 1. Смешайте творожный сыр, 
            рубленую петрушку и чеснок, и смажьте хлеб. 2. Сверху выложите тонкие ломтики авокадо, 
            а на него — кружочки огурца и помидоров. 3. Посыпьте готовые бутерброды специями. 
            """,
            """
            Бутерброды со шпротами и яйцом. Ингредиенты: 1 банка шпрот, 2 яйца, 
            2 помидора, хлеб, зелень, 0,5 лимона, 1 ст. л. майонеза. 
            1 Приготовление: 1. Подсушите хлеб на сковороде и слегка 
            смажьте майонезом. 2. Отварите яйца и 
            нарежьте кружочками с помидорами. 3. Выложите их на хлеб, 
            сверху разложите шпроты и добавьте маленький ломтик лимона
            """
        ]

        items = await self.repository.get_all(device_id)

        if len(items) >= 2:
            return choice(RANDOM_RECIPE)

        return []