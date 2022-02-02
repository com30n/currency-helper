from fastapi import APIRouter

from . import currencies

router = APIRouter()
router.include_router(currencies.router, tags=["currencies"])
