from ast import In
from fastapi import APIRouter
from endpoints import Index, Photo

router = APIRouter()
router.include_router(Index.router)
router.include_router(Photo.router)
