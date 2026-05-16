from datetime import datetime
from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import UploadFile, File, Depends, APIRouter, HTTPException, status
from fastapi.responses import FileResponse
import shutil
from app.models.photo import Photo
from bson.objectid import ObjectId
import os
from app.crud.photo import get_photo_by_id, insert_photo


router = APIRouter(
    prefix="/photo",
    tags=["Photo"],
    responses={404: {"description": "Not found"}},
)


@router.get(path="/get_photo/{id}")
async def retrieve_photo(id: str, db: AsyncIOMotorClient = Depends(get_database)): # type: ignore
    """
    Retrieve a photo by id and return the photo metadata as JSON. If the photo is not found, return a 404 error.
    """
    try:
        photo = await get_photo_by_id(db, id)

        print(photo)
        if photo is None:
            raise HTTPException(status_code=404, detail="Photo not found")
        return {**photo,"_id": str(photo["_id"])}
    except Exception as e:
        print(e)


@router.get(path="/image/{id}")
async def retrieve_image(id: str, db: AsyncIOMotorClient = Depends(get_database)): # type: ignore
    """
    Retrieve a photo by id and return the photo as an image file. If the photo is not found, return a 404 error."""
    try:
        image = await get_photo_by_id(db, id)
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")
        path = os.path.dirname("storage/imgs/")
        return FileResponse(os.path.join(path, image["filename"]))
    except Exception as e:
        print(e)


@router.post(path="/upload", tags=["Photo"], summary="Upload Photo", description="Upload Photo", response_description="Upload Photo",status_code=status.HTTP_201_CREATED)
async def uploadImage(
    image: UploadFile = File(...),
    db: AsyncIOMotorClient = Depends(get_database)): # type: ignore
    """
    Upload a photo and save the photo metadata in MongoDB. The photo file will be saved in the storage/imgs/ directory. The photo metadata will be saved in the photos collection in MongoDB. The photo metadata will include the original filename, the mimetype, the size, the path, the filename and the created date. The response will include the id of the inserted photo metadata."""

    path = f"storage/imgs/{image.filename}"
    print(image.filename)
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
        photo = Photo(
            photoname=image.filename,
            originalname=image.filename,
            mimetype=image.content_type,
            size= round(buffer.__sizeof__()/1024, ndigits=3),
            path=f"../storage/imgs/{image.filename}",
            filename=image.filename,
            created=datetime.now()
        )
    buffer.close()

    insertion = await insert_photo(db, photo)
    return {
        "id": str(insertion.inserted_id)
    }

