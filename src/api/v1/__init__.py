from fastapi import APIRouter

from . import currencies, spot_prices

router = APIRouter()
router.include_router(currencies.router, tags=["currencies"])
router.include_router(spot_prices.router, tags=["spot_prices"])
