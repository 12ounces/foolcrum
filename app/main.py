from fastapi import FastAPI
from core.database import engine
from models import Base

app = FastAPI(title='FoolCrum', version='0.0.1')

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {'message': 'CRM запущена', 'version' : '0.0.1'}
