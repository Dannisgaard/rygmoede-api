from typing import List, Optional
from .rwmodel import RWModel
from .dbmodel import DateTimeModelMixin, DBModelMixin

class Beer(RWModel):
    brewery: str
    chosenBy: str
    numberOfStars: float
    tagList: List[str]
    etiquetteImage: str


class BeerInDb(DateTimeModelMixin, Beer):
    pass