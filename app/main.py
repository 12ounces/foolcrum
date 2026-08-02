from fastapi import FastAPI
from core.database import engine
from models import Base

from api.v1 import contacts


app = FastAPI(title='FoolCrum', version='0.0.1')

app.include_router(contacts.router, prefix='/contacts', tags=['contacts'])

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {'message': 'CRM запущена', 'version' : '0.0.2'}


