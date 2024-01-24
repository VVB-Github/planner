from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.users import user_router
from routes.events import event_router
from database.connection import init_db_1

import uvicorn

app = FastAPI()

# Register routes

app.include_router(user_router,  prefix="/user")
app.include_router(event_router, prefix="/event")

@app.on_event("startup")
async def init_db():
    await init_db_1()

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)