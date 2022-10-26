import datetime
from bson.objectid import ObjectId
from app.core.config import database_name, photos_collection_name, persons_collection_name

from app.models.person import (
    Person,
    PersonInDb,
    ManyPersonsInResponse,
    PersonInUpdate,
)
from app.db.mongodb import AsyncIOMotorClient
from app.models.photo import Photo


async def get_photo_by_id(conn: AsyncIOMotorClient, id: str):
    photo = await conn[database_name][photos_collection_name].find_one({"_id": ObjectId(id)})
    if photo:
        return photo
    else:
        return None


async def insert_photo(conn: AsyncIOMotorClient, photo: Photo):
    photo = await conn[database_name][photos_collection_name].insert_one(photo.dict())
    return photo
