from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables




@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова к работе')
    yield
    print('Выключение')


app = FastAPI(lifespan=lifespan)