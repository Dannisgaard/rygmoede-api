from fastapi import APIRouter, Depends

from app.crud.tag import fetch_all_tags
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.tag import TagsList

router = APIRouter(
    prefix="/tag",

    tags=["Tags"],
    responses={404: {"description": "Not found"}},
)

@router.get("/tags", response_model=TagsList, tags=["Tags"])
async def get_all_tags(db: AsyncIOMotorClient = Depends(get_database)):
    tags = await fetch_all_tags(db)
    return TagsList(tags=[tag.tag for tag in tags])