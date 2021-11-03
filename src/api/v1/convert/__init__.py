from fastapi import APIRouter

from . import convert

router = APIRouter()
router.include_router(convert.router)
