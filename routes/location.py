from typing import List
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, status
from models.location import Location, LocationUpdate
# обьект для управления соединением с базой данных
from database.connection import Database

location_router = APIRouter(
    tags = ["Locations"]
)

location_database = Database(Location)

# маршрут получения всех локаций
@location_router.get("/get_all", response_model = List[Location])
async def get_all_locations() -> List[Location]:
    locations = await location_database.get_all()
    return locations

# маршрут получения локации по id
@location_router.get("/{id}", response_model=Location)
async def get_location_by_id(id:PydanticObjectId) -> Location:
    location = await location_database.get(id)
    return location

# маршрут добавления локации
'''
# аннотация Body используется для определения тела запроса
# (request body) в маршрутах API. Это позволяет вашему приложению
# обрабатывать данные, переданные в запросе, например, при создании
# или обновлении ресурса.
'''
@location_router.post("/new")
async def add_location(location:Location = Body(...)) -> dict:
    await location_database.save(location)
    return {"message":"location added"}

# маршрут модификации локации
@location_router.put("/new/{id}", response_model = Location)
async def update_location(id:PydanticObjectId,location:Location)-> Location:
    updated_location = await location_database.update(id, location)
    if not updated_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "location with such id does not exist"
        )
    return updated_location

# маршрут удаления локации
@location_router.delete("/new/{id}")
async def add_location(id:PydanticObjectId) -> dict:
    location = await location_database.delete(id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "location with such id is not found"
        )
    return {"message":"location deleted"}
