from fastapi import APIRouter

from . import convert, get

router = APIRouter()
router.include_router(get.router, prefix="/get", tags=["currencies"])
router.include_router(convert.router, prefix="/convert", tags=["convert"])
