from tracemalloc import start
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, Path, Query, HTTPException
from fastapi.responses import PlainTextResponse
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
async def retrieve_meeting_by_date(date: str,  db: AsyncIOMotorClient = Depends(get_database)) -> MeetingInDb: # type: ignore
    """
    Retrieve a meeting by exact date
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
        db: AsyncIOMotorClient = Depends(get_database)): # type: ignore
    """Create a new meeting. If a meeting with the same date already exists, return a 422 error.
    """

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
async def get_meetings(db: AsyncIOMotorClient = Depends(get_database)): # type: ignore
    dbmeetings = await get_all_meetings(db)
    """Get all meetings. Return a list of meetings."""

    return create_aliased_response(ManyMeetingsInResponse(meetings=dbmeetings))


@router.get("/meetings_markdown", response_class=PlainTextResponse, tags=["Meeting"])
async def get_meetings_markdown(db: AsyncIOMotorClient = Depends(get_database)):
    """Get all meetings and return them in Markdown format."""
    dbmeetings = await get_all_meetings(db)
    markdown = "# Oversigt over alle rygmøder\n"
    markdown += "========================\n"
    for meeting in dbmeetings:
        markdown += f"### Møde den {meeting.date.strftime('%d-%m-%Y')} hos {meeting.host}\n"
        for beer in meeting.beers:
            markdown += f"- Øl fra bryggeriet {beer.brewery} valgt af {beer.chosenBy} her fået {beer.numberOfStars} stjerner <br>\n"
            if beer.tagList:
                markdown += f"  - Smag: {', '.join(beer.tagList)}<br>\n"
            markdown += f"<img src='https://rygmoede.dannisgaard.dk/api/photo/image/{beer.etiquetteImage}' alt='Foto af etiket' style='width: 300px;'></img>\n"
        markdown += "---\n"
        markdown += "\n"
    return markdown


@router.get("/meetings_count", response_class=PlainTextResponse, tags=["Meeting"])
async def get_meetings_count(db: AsyncIOMotorClient = Depends(get_database)):
    """Get the count of all meetings."""
    dbmeetings = await get_all_meetings(db)
    return str(len(dbmeetings))


@router.get("/meetings_between", response_model=ManyMeetingsInResponse, tags=["Meeting"])
async def get_meetings_between_dates(start_date: str, end_date: str, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Get the data with meetings between two dates.
    Dates must be in format YYYY.MM.DD (e.g. 2026.05.16)
    """
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, "%Y.%m.%d")
        end = datetime.strptime(end_date, "%Y.%m.%d")
    except ValueError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Dates must be in format YYYY.MM.DD (e.g. 2026.05.16)")
    dbmeetings = await get_all_meetings(db)
    filtered_meetings = [meeting for meeting in dbmeetings if start <= meeting.date <= end]
    return create_aliased_response(ManyMeetingsInResponse(meetings=filtered_meetings))


@router.get("/beers_selected_by_person", response_model=List[Beer], tags=["Meeting"])
async def get_beers_selected_by_person(name: str, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Get all beers selected by a person. Return a list of beers.
    """
    dbmeetings = await get_all_meetings(db)
    beers = []
    for meeting in dbmeetings:
        for beer in meeting.beers:
            if beer.chosenBy.lower() == name.lower():
                beers.append(beer)
    return create_aliased_response(beers)


@router.get("/beers_selected_by_person_between", response_model=List[Beer], tags=["Meeting"])
async def get_beers_selected_by_person_between_dates(name: str, start_date: str, end_date: str, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Get all beers selected by a person between two dates. Return a list of beers.
    """
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, "%Y.%m.%d")
        end = datetime.strptime(end_date, "%Y.%m.%d")
    except ValueError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Dates must be in format YYYY.MM.DD (e.g. 2026.05.16)")
    dbmeetings = await get_all_meetings(db)
    filtered_meetings = [meeting for meeting in dbmeetings if start <= meeting.date <= end]
    beers = []
    for meeting in filtered_meetings:
        for beer in meeting.beers:
            if beer.chosenBy.lower() == name.lower():
                beers.append(beer)
    return create_aliased_response(beers)
   

@router.get("/beers_selected_by_min_stars_between", response_model=List[Beer], tags=["Meeting"])
async def get_beers_selected_by_min_stars_between(start_date: str, end_date: str, min_stars: int, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Get all beers with a certain number of stars or more between two dates. Return a list of beers.
    """
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, "%Y.%m.%d")
        end = datetime.strptime(end_date, "%Y.%m.%d")
    except ValueError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Dates must be in format YYYY.MM.DD (e.g. 2026.05.16)")
    dbmeetings = await get_all_meetings(db)
    filtered_meetings = [meeting for meeting in dbmeetings if start <= meeting.date <= end]
    beers = []
    for meeting in filtered_meetings:
        for beer in meeting.beers:
            if beer.numberOfStars >= min_stars:
                beers.append(beer)
    return create_aliased_response(beers)


@router.get("/beers_selected_by_min_stars", response_model=List[Beer], tags=["Meeting"])
async def get_beers_selected_by_min_stars(min_stars: int, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Get all beers with a certain number of stars or more. Return a list of beers.
    """
    dbmeetings = await get_all_meetings(db)
    beers = []
    for meeting in dbmeetings:
        for beer in meeting.beers:
            if beer.numberOfStars >= min_stars:
                beers.append(beer)
    return create_aliased_response(beers)


@router.get("/beers_selected_by_max_stars", response_model=List[Beer], tags=["Meeting"])
async def get_beers_selected_by_max_stars(max_stars: int, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Get all beers with a certain number of stars or less. Return a list of beers.
    """
    dbmeetings = await get_all_meetings(db)
    beers = []
    for meeting in dbmeetings:
        for beer in meeting.beers:
            if beer.numberOfStars <= max_stars:
                beers.append(beer)
    return create_aliased_response(beers)


@router.get("/beers_by_tag", response_model=List[Beer], tags=["Meeting"])
async def get_beers_by_tag(tag: str, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Get all beers matching a tag (case-insensitive, partial match).
    E.g. tag=bitter matches 'Bitter', 'Semi-bitter', 'bittersweet'.
    """
    dbmeetings = await get_all_meetings(db)
    tag_lower = tag.lower()
    beers = []
    for meeting in dbmeetings:
        for beer in meeting.beers:
            if any(tag_lower in t.lower() for t in beer.tagList):
                beers.append(beer)
    return create_aliased_response(beers)