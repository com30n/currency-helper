from fastapi import APIRouter

from . import currency

router = APIRouter()
router.include_router(currency.router, tags=["convert"])
