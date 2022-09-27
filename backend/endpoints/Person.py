from connection import conndb
from fastapi import APIRouter, Body, Depends, Path, Query, HTTPException
from fastapi.responses import FileResponse
import shutil
from app.crud.person import create_person, get_person_by_name
from app.core.utils import create_aliased_response
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.person import Person
from app.models.person import (
    Person,
    PersonInDb,
    PersonInResponse,
    PersonInUpdate,
)
from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


router = APIRouter(
    prefix="/person",

    tags=["Person"],
    responses={404: {"description": "Not found"}},
)

@router.get(path="/get_person/{id}")
def retrieve_photo(id: str):
    """
    Retrieve a person by id
    """
    try:
        client = conndb.Connection()
        client.connect()
        person = client.get_collection("rygmoede", "person").find_one({"_id": ObjectId(id)})
        if person is None:
            raise HTTPException(status_code=404, detail="Person not found")
        return {**person,"_id": str(person["_id"])}
    except Exception as e:
        print(e)


@router.post("",
    response_model=Person,
    tags=["Person"],
    status_code=HTTP_201_CREATED,
)
async def create_new_person(
        person: Person = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
):
    person_by_name = await get_person_by_name(db, person.name)
    if person_by_name:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Kan ikke gemme person med navn='{person_by_name.name}'",
        )

    dbperson = await create_person(db, person)
    return create_aliased_response(PersonInResponse(person=dbperson))

