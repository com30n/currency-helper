from fastapi import APIRouter

from . import ping, metrics

router = APIRouter()

router.include_router(ping.router)
router.include_router(metrics.router)
