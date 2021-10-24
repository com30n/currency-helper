from fastapi import APIRouter

from . import currencies, spot

router = APIRouter()
router.include_router(currencies.router)
router.include_router(spot.router)
