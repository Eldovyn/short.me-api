from ..databases import UserDatabase
from flask import jsonify


class ProfileController:
    @staticmethod
    async def user_me(user):
        return (
            jsonify(
                {
                    "message": "successfully get user",
                    "data": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                        "is_active": user.is_active,
                    },
                }
            ),
            200,
        )
