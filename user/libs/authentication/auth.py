from datetime import datetime

import jwt

from user.libs.redis.redis import MasterRedis
from user.models import User
from user.libs.constants.constants import UserConstant
from rest_framework.response import Response
from rest_framework import status


def authentication(function):
    def wrapper(self, request, *args, **kwargs):
        response = Response()
        redis = MasterRedis()
        token = request.headers.get("Authorization")
        if token:
            try:

                payload = jwt.decode(token, "secret", algorithms=['HS256'])
                user = User.objects.filter(id=payload['id']).first()

                key = str(user.id) + UserConstant.REDIS_USER_KEY

                if redis.get_keys(key):
                    return function(self, request)
                else:
                    response.data = {
                        "message": "Unauthorized",
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                    return Response(response.data, status=status.HTTP_400_BAD_REQUEST)
            except Exception:

                response.data = {
                    "message": "Wrong Token",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response.data, status=status.HTTP_400_BAD_REQUEST)
        else:

            response.data = {
                "message": "Unauthorized",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response.data, status=status.HTTP_400_BAD_REQUEST)

    return wrapper