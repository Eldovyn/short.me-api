from functools import wraps
from flask import request, jsonify
from ..utils import AuthJwt
import asyncio
from ..models import UserModel, BlacklistTokenModel


def jwt_required():
    def decorator(f):
        async def async_handler(*args, **kwargs):
            result = _verify_jwt()
            if isinstance(result, tuple):
                return result
            return await f(*args, **kwargs)

        def sync_handler(*args, **kwargs):
            result = _verify_jwt()
            if isinstance(result, tuple):
                return result
            return f(*args, **kwargs)

        @wraps(f)
        def _verify_jwt():
            auth_header = request.headers.get("Authorization")
            timestamp = request.timestamp
            if not auth_header:
                return (
                    jsonify(
                        {
                            "message": "invalid authorization header",
                            "errors": {"authorization": ["IS_INVALID"]},
                        }
                    ),
                    401,
                )

            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return (
                    jsonify(
                        {
                            "message": "invalid authorization header",
                            "errors": {"authorization": ["IS_INVALID"]},
                        }
                    ),
                    401,
                )

            token = parts[1]
            payload = AuthJwt.verify_token(token)
            if payload is None:
                return (
                    jsonify(
                        {
                            "message": "invalid or expired token",
                            "errors": {"token": ["IS_INVALID"]},
                        }
                    ),
                    401,
                )

            user_id = payload.get("sub")
            iat = payload.get("iat")
            if not user_id:
                return (
                    jsonify(
                        {
                            "message": "invalid or expired token",
                            "errors": {"token": ["IS_INVALID"]},
                        }
                    ),
                    401,
                )

            if not (user_data := UserModel.objects(id=user_id).first()):
                return (
                    jsonify(
                        {
                            "message": "invalid or expired token",
                            "errors": {"token": ["IS_INVALID"]},
                        }
                    ),
                    401,
                )

            if not iat > user_data.updated_at:
                return (
                    jsonify(
                        {
                            "message": "invalid or expired token",
                            "errors": {"token": ["IS_INVALID"]},
                        }
                    ),
                    401,
                )

            if token_blacklist := BlacklistTokenModel.objects(created_at=iat).first():
                return (
                    jsonify(
                        {
                            "message": "invalid or expired token",
                            "errors": {"token": ["IS_INVALID"]},
                        }
                    ),
                    401,
                )

            if not user_data.is_active:
                return (
                    jsonify(
                        {
                            "message": "user is not active",
                            "errors": {"user": ["NOT_ACTIVE"]},
                        }
                    ),
                    401,
                )

            request.user = user_data
            request.token = payload

            return True

        if asyncio.iscoroutinefunction(f):
            return wraps(f)(async_handler)
        else:
            return wraps(f)(sync_handler)

    return decorator
