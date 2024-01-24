from typing import List
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event, EventUpdate
# обьект для управления соединением с базой данных
from database.connection import Database

event_router = APIRouter(
    tags=["Events"]
)

# event_databse - это наш класс database (который мы написала), с 
# переданным в него моделью, а именно моделью - Event
event_database = Database(Event)

# Путь получения всех записей
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    # используем методы, которые мы же и обьявили
    events = await event_database.get_all()
    return events

# получение записи по id
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

# путь добавления
@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    # в классе для этого выполняется строка: await document.create()
    await event_database.save(body)
    return {
        "message": "Event created successfully"
    }

# путь удаления
@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return {"message":"Event deleted successfully"}

# путь обновления
@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Event with supplied ID does not exist"
        )
    return updated_event






