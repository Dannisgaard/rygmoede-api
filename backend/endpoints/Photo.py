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
async def retrieve_photo(id: str, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Retrieve a photo by id
    """
    try:
        # client = conndb.Connection()
        # client.connect()
        # photo = client.get_collection("rygmoede", "photos").find_one({"_id": ObjectId(id)})
        photo = await get_photo_by_id(db, id)

        print(photo)
        if photo is None:
            raise HTTPException(status_code=404, detail="Photo not found")
        return {**photo,"_id": str(photo["_id"])}
    except Exception as e:
        print(e)


@router.get(path="/image/{id}")
async def retrieve_image(id: str, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        # client = conndb.Connection()
        # client.connect()
        # collection = client.get_collection("rygmoede", "photos")
        # image = collection.find_one({"_id": ObjectId(id)})
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
    db: AsyncIOMotorClient = Depends(get_database)):

    # client = conndb.Connection()
    # client.connect()
    # collection = client.get_collection("rygmoede", "photos")

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
        )
    buffer.close()

    # insertion = collection.insert_one(photo.dict()).inserted_id
    insertion = await insert_photo(db, photo)
    return {
        "id": str(insertion.inserted_id)
    }

