from fastapi import APIRouter
from .user_router import router as user_router
from .menu_router import router as menu_router

router = APIRouter(prefix="/api")
router.include_router(user_router, tags=["user"])
router.include_router(menu_router, tags=["menu"])
