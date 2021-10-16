from fastapi import APIRouter

from . import spot_prices

router = APIRouter()
router.include_router(spot_prices.router, tags=["spot_prices"])
