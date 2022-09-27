from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DBModelMixin(DateTimeModelMixin):
    id: Optional[UUID] = None
