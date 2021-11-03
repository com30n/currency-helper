from fastapi import APIRouter

from . import crypto, fiat, convert

router = APIRouter()
router.include_router(crypto.router, prefix="/crypto", tags=["crypto"])
router.include_router(fiat.router, prefix="/fiat", tags=["fiat"])
router.include_router(convert.router, prefix="/convert", tags=["convert"])
