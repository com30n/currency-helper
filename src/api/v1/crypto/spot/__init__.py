from fastapi import APIRouter

from . import spot_prices

router = APIRouter()
router.include_router(spot_prices.router, prefix="/spot", tags=["spot_prices"])
