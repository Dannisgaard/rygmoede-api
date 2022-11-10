from datetime import date, datetime
from pydantic import BaseModel, Field
class Photo(BaseModel):
    photoname: str
    originalname: str
    mimetype: str
    size: int
    path: str
    filename: str
    created: datetime = Field(default=datetime.now())