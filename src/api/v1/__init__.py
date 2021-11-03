from fastapi import APIRouter

from . import convert, currencies

router = APIRouter()
router.include_router(currencies.router, tags=["currencies"])
router.include_router(convert.router, tags=["convert"])
