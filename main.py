import asyncio
import uvicorn as uvicorn
from fastapi import FastAPI
from bot.cashbot import CashBot


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "FastAPI + aiogram bot is running!"}


async def start_bot():
    """"""
    bot = CashBot()
    await bot.on_start()


@app.on_event("startup")
async def start_app():
    """Запуск сервера"""
    asyncio.create_task(start_bot())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
