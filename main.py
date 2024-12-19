import random
from abc import abstractmethod
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import FastAPI, Header, Depends, File
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from app.device_feature.domain import Device, WrongDeviceID
from app.device_feature.service import DeviceService
from app.product_feature.domain import Product, ProductCreate
from app.product_feature.service import ProductFeatureService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



@app.post('/register-device')
async def register_device_id(device_id: str,
                             device_service = Depends(DeviceService) ):
    """Регистрация холодильника в системе"""
    try:
        device = await device_service.register_device(device_id)
        return {"success": True, "private_key": device.private_key}
    except Exception as e:
        print(e)
        return {"success": False}

@app.post('/login')
async def login(request: Request,
                device_id: str, private_key: str, device_service: DeviceService = Depends(DeviceService)):
    try:
        access_token, refresh_token = await device_service.authenticate_device(device_id, private_key,
                                                                               request.client.host)

        return {"access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        print(e)
        return {"success": False}

@app.post('/refresh')
async def refresh_token(request: Request,
                        refresh_token: str,
                        device_service: DeviceService = Depends(DeviceService)):
    try:
        access_token, refresh_token = await device_service.rotate_token(refresh_token, request.client.host)

        return {"access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        print(e)
        return {"success": False}




@app.post('/insert-product')
async def insert_product( request: Request,
                          product: ProductCreate,
                          x_token = Header(...),
                          device_service: DeviceService = Depends(DeviceService),
                          product_service: ProductFeatureService = Depends(ProductFeatureService)):

    """Вставка продукта в бд"""

    try:
        device = await device_service.get_device_by_access_token(x_token, request.client.host)

        product = Product(**product.model_dump(), device_id=device.device_id)

        created_product = await product_service.insert(product)

        return created_product

    except Exception as e:
        print(e)
        return {"success": False}




@app.get('/get-products')
async def get_products(request: Request,
                       x_token = Header(...),
                       device_service: DeviceService = Depends(DeviceService),
                       product_service: ProductFeatureService = Depends(ProductFeatureService)
                       ):

    """Получить все продукты в холодильнике"""

    try:
        device = await device_service.get_device_by_access_token(x_token, request.client.host)

        products = await product_service.list(device.device_id)

        return products

    except Exception as e:
        print(e)
        return {"success": False}


@app.get('/get-random-recipe')
async def get_recipe(request: Request,
                     x_token = Header(...),
                     device_service: DeviceService = Depends(DeviceService),
                     product_service: ProductFeatureService = Depends(ProductFeatureService)
                     ):
    """Получить рандомный рецепт"""
    try:
        device = await device_service.get_device_by_access_token(x_token, request.client.host)

        products = await product_service.get_recipe(device.device_id)

        return products

    except Exception as e:
        print(e)
        return {"success": False}


@app.post('/detect-product')
async def detect_product(request: Request,file: Annotated[bytes, File()],
                   x_token = Header(...),
                   device_service: DeviceService = Depends(DeviceService),
                   product_service: ProductFeatureService = Depends(ProductFeatureService)
                   ):

    """Распознания продукта на изображении"""

    try:
        KB = 1024

        if len(file) < KB:
            return {"success": False, "msg": "Не удалось распознать"}

        names = ['Молоко', 'Сыр', 'Мясо']

        device = await device_service.get_device_by_access_token(x_token, request.client.host)

        product = Product(
            device_id=device.device_id,
            name=random.choice(names),
            produced_at=datetime.now() - timedelta(random.randint(1,3)),
            expire_at=datetime.now() + timedelta(random.randint(1,3)),
        )

        created_product = await product_service.insert(product)

        return created_product

    except Exception as e:
        print(e)
        return {"success": False}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)