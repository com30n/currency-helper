from fastapi import APIRouter

from . import private  # noqa: F401
from . import v1  # noqa: F401

router = APIRouter()

router.include_router(v1.router, prefix="/api/v1", tags=["v1"])
router.include_router(private.router, prefix="/-", tags=["private"])
