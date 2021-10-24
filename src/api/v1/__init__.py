from fastapi import APIRouter

from . import crypto

router = APIRouter()
router.include_router(crypto.router, prefix="/crypto", tags=["crypto"])
