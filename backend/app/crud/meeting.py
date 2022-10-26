import datetime
from typing import Optional
from app.core.config import database_name, meetings_collection_name
import uuid
from uuid import UUID
from app.models.meeting import (
    Meeting,
    ManyMeetingsInResponse,
    MeetingInDb,
)
from app.db.mongodb import AsyncIOMotorClient


async def create_meeting(conn: AsyncIOMotorClient, meeting: Meeting,
                              username: Optional[str] = None) -> MeetingInDb:
    meeeting_doc = meeting.dict()
    meeeting_doc["updated_at"] = datetime.datetime.now()
    meeeting_doc["created_at"] = datetime.datetime.now()
    await conn[database_name][meetings_collection_name].insert_one(meeeting_doc)

    return MeetingInDb(**meeeting_doc)


async def get_all_meetings(conn: AsyncIOMotorClient) -> ManyMeetingsInResponse:
    meetings: ManyMeetingsInResponse = []
    rows = conn[database_name][meetings_collection_name].find()
    async for row in rows:
        meetings.append(Meeting(**row, ))
    return meetings


async def get_meeting_by_date(conn: AsyncIOMotorClient,
                           date: datetime,
                           username: Optional[str] = None) -> MeetingInDb:
    query = {"created_at": {
            "$gt": date - datetime.timedelta(days=1),
            "$lt": date + datetime.timedelta(days=1),
    }}
    meeting_docs = await conn[database_name][meetings_collection_name].find(query).to_list(1)
    
    for d in meeting_docs:
        print(d)


    if meeting_docs:
        return MeetingInDb(**meeting_docs[0])
    else:
        return None


# def get_meeting_by_date(conn: AsyncIOMotorClient,
#                            date: datetime,
#                            username: Optional[str] = None) -> MeetingInDb:
#     query = {"created_at": {
#             "$gt": date - datetime.timedelta(days=1),
#             "$lt": date + datetime.timedelta(days=1),
#     }}
#     meeting_docs = conn[database_name][meetings_collection_name].find(query).to_list(2)
    
#     for d in meeting_docs:
#         print(d)


#     if meeting_docs:
#         return MeetingInDb(**meeting_docs[0])
#     else:
#         return None