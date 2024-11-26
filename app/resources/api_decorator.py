import jwt
import logging
from functools import wraps
from flask import request
from flask_api import status
from jwt.exceptions import PyJWTError, ExpiredSignatureError

from resources.connections import JWT_SECRET


def api_endpoint():

    def wrapper(f):
        @wraps(f)
        def decorator_f(*args, **kwargs):
            try:
                if JWT_SECRET:
                    auth_type, auth_token = request.headers.get(
                        "Authorization", ""
                    ).split()
                    jwt.decode(
                        jwt=auth_token,
                        key=JWT_SECRET,
                        algorithms="HS256",
                        issuer="noharm",
                    )

                return f(*args, **kwargs)

            except ExpiredSignatureError:
                return {
                    "status": "error",
                    "message": "Token expirado",
                }, status.HTTP_401_UNAUTHORIZED

            except PyJWTError as e:
                logging.basicConfig()
                logger = logging.getLogger("noharm.getname")
                logger.exception(str(e))

                return {
                    "status": "error",
                    "message": "Erro de autenticação. Consulte os logs para mais detalhes.",
                }, status.HTTP_401_UNAUTHORIZED

            except Exception as e:
                logging.basicConfig()
                logger = logging.getLogger("noharm.getname")
                logger.exception(str(e))

                return {
                    "status": "error",
                    "message": "Erro inesperado. Consulte os logs para mais detalhes.",
                }, status.HTTP_500_INTERNAL_SERVER_ERROR

        return decorator_f

    return wrapper
