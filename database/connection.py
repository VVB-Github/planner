# init_beanie - это функция из библиотеки Beanie, которая предназначена для
# инициализации соединения и конфигурации для использования MongoDB с асинхронным
# драйвером motor.
from beanie import init_beanie 

# обычно в MongoDB для уникальной идентификации документов
# используется тип данных ObjectID. PydanticObjectId обеспечивает 
# взаимодействие с такими идентификаторами в Pydantic-моделях
from beanie import PydanticObjectId
from models.users import User
from models.events import Event

import motor, motor.motor_asyncio, beanie

# Асинхронная версия клиента MongoDB
from motor.motor_asyncio import AsyncIOMotorClient 
from typing import Optional, List

# Универсальный тип, который может принимать значения любого типа
from typing import Any

# BaseSettings из модуля pydantic используется для создания классов 
# настроек (settings) с использованием Pydantic
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# класс для работы с БД
class Database:
    def __init__(self, model):
        self.model = model
    
    # Метод для добавления записи в коллекцию базы данных  
    async def save(self, document) -> None:
        await document.create()
        return 

    # метод получения записи по id
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    
    # метод получения всех записей
    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs
    
    async def update(self, id:PydanticObjectId, body:BaseModel) -> Any:
        doc_id = id
        
        # возможно вместо body.dict() надо использовать 
        # model.dump()
        des_body = body.dict()
        
        # Это создает новый словарь с использованием генератора словаря.
        # В этой части кода происходит итерация по парам ключ-значение
        # из des_body.items(), и только те пары, где значение (v)
        # не равно None, включаются в новый словарь.
        des_body = {k:v for k,v in des_body.items() if v is not None}
        
        # Создается словарь update_query с ключом "$set",
        # указывающим на оператор $set в MongoDB, который
        # используется для обновления значений полей в документе.
        update_query = {"$set": {field: value for field, value in 
                                 des_body.items()}}
        
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
    
    async def delete(self, id:PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True 

# функция подключения БД
async def init_db_1():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    await beanie.init_beanie(
        database=client.db_name,
        document_models=[User, Event]
    )
        
        
