from typing import List

from app.db.mongodb import AsyncIOMotorClient
from app.models.tag import TagInDB
from app.core.config import database_name, tags_collection_name


async def fetch_all_tags(conn: AsyncIOMotorClient) -> List[TagInDB]:
    tags = []
    rows = conn[database_name][tags_collection_name].find()
    async for row in rows:
        tags.append(TagInDB(**row))

    return tags


async def create_tags_that_not_exist(conn: AsyncIOMotorClient,
                                     tags: List[str]):
    for tag in tags:
        has_tag = await conn[database_name][tags_collection_name].find_one(
            {'tag': tag})
        if not has_tag:
            await conn[database_name][tags_collection_name].insert_one(
                {"tag": tag})
