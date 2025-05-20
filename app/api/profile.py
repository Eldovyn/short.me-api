from flask import Blueprint, request
from ..controllers import ProfileController
from ..utils import jwt_required

profile_router = Blueprint("profile_router", __name__)


@profile_router.patch("/short.me/user/username")
@jwt_required()
async def update_username():
    user = request.user
    json = request.json
    username = json.get("username", "")
    return await ProfileController.update_username(user, username)


@profile_router.patch("/short.me/user/password")
@jwt_required()
async def update_password():
    user = request.user
    json = request.json
    timestamp = request.timestamp
    password = json.get("password", "")
    confirm_password = json.get("confirm_password", "")
    return await ProfileController.update_password(
        user, password, confirm_password, timestamp
    )


@profile_router.patch("/short.me/user/email")
@jwt_required()
async def update_email():
    user = request.user
    json = request.json
    timestamp = request.timestamp
    email = json.get("email", "")
    otp = json.get("otp", "")
    return await ProfileController.update_email(user, email, otp, timestamp)
