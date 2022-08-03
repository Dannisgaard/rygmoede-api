from uvicorn import Config
from routes.api import router as api_router
from fastapi import FastAPI
from config import config
from fastapi.middleware.cors import CORSMiddleware
from connection import conndb


app = FastAPI()

origins = ["http://192.168.1.23:8000", config.config().API_URL , config.config().CLIENT_SIDE_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)