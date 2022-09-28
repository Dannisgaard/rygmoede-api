from typing import List, Optional
from .rwmodel import RWModel
from .dbmodel import DateTimeModelMixin, DBModelMixin

class Person(RWModel):
    name: str

class PersonInDb(DateTimeModelMixin, Person):
    pass

class PersonInResponse(RWModel):
    person: Person

class PersonInUpdate(RWModel):
    name: Optional[str] = None

class ManyPersonsInResponse(RWModel):
    persons: List[Person]