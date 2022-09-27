import logging

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from app.db.mongodb import db


async def connect_to_mongo():
    logging.info("Try to connect to mongo")
    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logging.info("connect to mongo！")


async def close_mongo_connection():
    logging.info("Try close mongo")
    db.client.close()
    logging.info("Mongo closed！")
