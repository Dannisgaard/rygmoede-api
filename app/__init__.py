from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.routes.api import router as api_router
from .core.config import ALLOWED_HOSTS, API_V1_STR, PROJECT_NAME
from .core.errors import http_422_error_handler, http_error_handler
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo
from fastapi.staticfiles import StaticFiles
from pathlib import Path

tags_metadata = [
    {
        "name": "Person",
        "description": "Manage persons in MongoDB.",
    },
    {
        "name": "Tags",
        "description":
        "Manage tag on beers, tag can be etc. 'sweet'",
    },
    {
        "name": "default",
        "description": "Just for check api runs.",
    },
]

app = FastAPI(
    title=PROJECT_NAME,
    description=
    "Api for Rygmøde app, remember witch beer we tasted.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)
current_file = Path(__file__)
project_root = current_file.parent.parent
project_root_absolute = project_root.resolve()
# static_root_absolute = project_root_absolute / "static"
# app.mount("/static", StaticFiles(directory=static_root_absolute), name="static")

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["https?://.*"]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=ALLOWED_HOSTS,
    allow_origin_regex=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY,
                          http_422_error_handler)

app.include_router(api_router, prefix=API_V1_STR)
