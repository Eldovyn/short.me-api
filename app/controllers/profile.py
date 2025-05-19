from ..databases import UserDatabase
from flask import jsonify


class ProfileController:
    @staticmethod
    async def user_me(user):
        if not "sub" in user:
            return (
                jsonify(
                    {
                        "message": "invalid or expired token",
                        "errors": {"token": ["IS_INVALID"]},
                    }
                ),
                401,
            )
        user_id = user["sub"]
        if not (user_data := await UserDatabase.get("by_user_id", user_id=user_id)):
            return (
                jsonify(
                    {
                        "message": "invalid or expired token",
                        "errors": {"token": ["IS_INVALID"]},
                    }
                ),
                401,
            )
        return (
            jsonify(
                {
                    "message": "successfully get user",
                    "data": {
                        "id": user_data.id,
                        "email": user_data.email,
                        "username": user_data.username,
                        "created_at": user_data.created_at,
                        "updated_at": user_data.updated_at,
                        "is_active": user_data.is_active,
                    },
                }
            ),
            200,
        )
