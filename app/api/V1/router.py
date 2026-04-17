from fastapi import APIRouter
from app.api.V1.endpoints import auth,homeapi, dbapi

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(homeapi.router)
api_router.include_router(dbapi.db_api)