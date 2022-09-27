import datetime
from typing import Optional
from app.core.config import database_name, users_collection_name, persons_collection_name
import uuid
from uuid import UUID
from app.models.person import (
    Person,
    PersonInDb,
    PersonInResponse,
    PersonInUpdate,
)
from app.db.mongodb import AsyncIOMotorClient

async def create_person(conn: AsyncIOMotorClient, person: Person,
                              username: Optional[str] = None) -> PersonInDb:
    person_doc = person.dict()
    person_doc["updated_at"] = datetime.datetime.now()
    person_doc["created_at"] = datetime.datetime.now()
    await conn[database_name][persons_collection_name].insert_one(person_doc)

    return PersonInDb(**person_doc)


async def get_person_by_name(conn: AsyncIOMotorClient,
                           name: str,
                           username: Optional[str] = None) -> PersonInDb:
    person_doc = await conn[database_name][persons_collection_name].find_one(
        {"name": name})
    if person_doc:
        return PersonInDb(**person_doc)
    else:
        return None


async def get_person_by_id(conn: AsyncIOMotorClient,
                         person_id: UUID,
                         username: Optional[str] = None) -> PersonInDb:
    person_doc = await conn[database_name][persons_collection_name].find_one(
        {"id": uuid.uuid4(person_id)})
    if person_doc:
        return PersonInDb(**person_doc)
    else:
        return None
