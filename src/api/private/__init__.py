from fastapi import APIRouter

from . import metrics, ping

router = APIRouter()

router.include_router(ping.router)
router.include_router(metrics.router)
