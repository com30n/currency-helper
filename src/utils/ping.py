from fastapi import Response, status


def ping(response: Response):
    response.status_code = status.HTTP_200_OK
    return Response("OK", status_code=status.HTTP_200_OK)
