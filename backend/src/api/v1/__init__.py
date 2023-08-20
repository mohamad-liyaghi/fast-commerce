from fastapi import APIRouter
from .auth import auth_router
from .profile import profile_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(profile_router, prefix="/profile")
