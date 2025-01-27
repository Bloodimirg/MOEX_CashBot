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


async def start_app():
    """Запуск сервера"""
    asyncio.create_task(start_bot())

    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(start_app())
