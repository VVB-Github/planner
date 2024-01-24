from typing import Optional, List 
from beanie import Document

# Linl используется для создания ссылок между документами в 
# MongoDB
from beanie import Link 
from pydantic import BaseModel, EmailStr 
from models.events import Event

class User(Document): 
    email: EmailStr 
    password: str 
    
    # строка events: Optional[List[Link[Event]]] говорит о том,
    # что в вашей модели данных есть атрибут events, который может
    # содержать список ссылок на события (Link[Event]), и он может
    # быть опциональным (может быть None).

    class Settings: 
        name = "users" 

    class Config: 
        schema_extra = { 
            "example": { 
                "email": "fastapi@packt.com", 
                "password": "strong!!!", 
            } 
        } 

class UserSignIn(BaseModel): 
    email: EmailStr 
    password: str