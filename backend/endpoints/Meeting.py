from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, Path, Query, HTTPException
from starlette.exceptions import HTTPException
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.core.utils import create_aliased_response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from app.models.meeting import (
    ManyMeetingsInResponse,
    Meeting,
    MeetingInDb
)
from app.models.beer import (
    Beer,
    BeerInDb
)
from app.crud.meeting import create_meeting, get_all_meetings, get_meeting_by_date
from app.crud.tag import create_tags_that_not_exist


router = APIRouter(
    prefix="/meeting",

    tags=["Meeting"],
    responses={404: {"description": "Not found"}},
)

@router.get(path="/get_meting_by_date/{date}", tags=["Meeting"])
async def retrieve_meeting_by_date(date: str,  db: AsyncIOMotorClient = Depends(get_database)) -> MeetingInDb:
    """
    Retrieve a meeting by date
    """
    try:
        person_by_name = await get_meeting_by_date(db, date)
        if person_by_name is None:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return MeetingInDb(**person_by_name.dict())
    except Exception as e:
        pass


@router.post(path="/create",
    response_model=MeetingInDb,
    tags=["Meeting"],
    status_code=HTTP_201_CREATED,
)
async def create_new_meeting(
        meeting: Meeting = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database)):
    meeting_by_date = await get_meeting_by_date(db, meeting.date)
    if meeting_by_date:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Kan ikke gemme meeting med dato='{meeting_by_date.date}'",
        )

    db_meeting = await create_meeting(db, meeting)
    for beer in db_meeting.beers:
        if beer.tagList:
            await create_tags_that_not_exist(db, beer.tagList)
    return create_aliased_response(db_meeting)


@router.get("/meetings", response_model=ManyMeetingsInResponse, tags=["Meeting"])
async def get_meetings(db: AsyncIOMotorClient = Depends(get_database)):
    dbmeetings = await get_all_meetings(db)
    return create_aliased_response(ManyMeetingsInResponse(meetings=dbmeetings))
