from datetime import datetime
from typing import List, Optional

from .beer import Beer
from .rwmodel import RWModel
from .dbmodel import DateTimeModelMixin, DBModelMixin

class Meeting(RWModel):
    host: str
    date: datetime
    beers: List[Beer]
    

class MeetingInDb(DateTimeModelMixin, Meeting):
    pass


class ManyMeetingsInResponse(RWModel):
    meetings: List[Meeting]