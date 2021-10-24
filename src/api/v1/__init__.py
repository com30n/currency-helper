from fastapi import APIRouter

from .crypto import currencies, spot

router = APIRouter()
router.include_router(currencies.router, tags=["currencies"])
router.include_router(spot.router, tags=["spot_prices"])
