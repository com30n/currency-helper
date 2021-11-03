from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/ping")
def ping(response: Response):
    response.status_code = status.HTTP_200_OK
    return Response("OK", status_code=status.HTTP_200_OK)
