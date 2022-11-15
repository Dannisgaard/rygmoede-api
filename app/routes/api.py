from ast import In
from fastapi import APIRouter
from endpoints import Index, Photo, Person, Meeting, Tag

router = APIRouter()
router.include_router(Index.router)
router.include_router(Photo.router)
router.include_router(Person.router)
router.include_router(Meeting.router)
router.include_router(Tag.router)
