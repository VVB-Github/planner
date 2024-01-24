from typing import List, Optional

# аналог BaseModel из pydantic, но для beanie и MongoDB
from beanie import Document
from pydantic import BaseModel

class Location(Document):
    title: str
    describtion: str
    tags: List[str]
    class Config:
        schema_extra = {
            "example": {
                "title": "restraunt",
                "description": "Cheap food",
                "tags": ["food", "cheap"],
            }
        }
    class Settings:
        name = "locations"
        
class LocationUpdate(Document):
    title: Optional[str]
    describtion: Optional[str]
    tags: Optional[List[str]]
    class Config:
        schema_extra = {
            "example": {
                "title": "restraunt",
                "description": "Cheap food",
                "tags": ["food", "cheap"],
            }
        }
    class Settings:
        name = "locations"        
         
