from connection import conndb
from fastapi import APIRouter, Body, Depends, Path, Query, HTTPException
from fastapi.responses import FileResponse
import shutil
from app.crud.person import create_person, get_person_by_name, get_all_persons
from app.core.utils import create_aliased_response
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.person import Person, ManyPersonsInResponse
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


@router.get(path="/get_person_by_name/{name}", tags=["Person"])
async def retrieve_person_by_name(name: str,  db: AsyncIOMotorClient = Depends(get_database)) -> PersonInDb:
    """
    Retrieve a person by name
    """
    try:
        person_by_name = await get_person_by_name(db, name)
        if person_by_name is None:
            raise HTTPException(status_code=404, detail="Person not found")
        return PersonInDb(**person_by_name.dict())
    except Exception as e:
        pass


@router.get("/persons", response_model=ManyPersonsInResponse, tags=["Person"])
async def get_persons(db: AsyncIOMotorClient = Depends(get_database)):
    dbpersons = await get_all_persons(db)
    return create_aliased_response(ManyPersonsInResponse(persons=dbpersons))


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

