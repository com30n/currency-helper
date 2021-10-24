from fastapi import APIRouter
from starlette_prometheus import metrics

router = APIRouter()

router.add_api_route("/metrics", metrics)
