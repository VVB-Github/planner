from typing import List, Optional

# аналог BaseModel из pydantic, но для beanie и MongoDB
from beanie import Document
from pydantic import BaseModel

class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    # schema_extra представляет пример данных для события, который может быть
    # использован при документации API или для создания тестовых данных
    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    
    # Этот атрибут устанавливает имя коллекции MongoDB, с которой будет связан документ.
    # В данном случае документы этого типа будут сохра-ся в колл-ю с именем events
    class Settings:
        name = "events"

# модель для операции Update. То же что и в классе Event, но все поля теперь - 
# Optional
class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI BookLaunch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
        
        
        