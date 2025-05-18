from flask import Blueprint, request
from ..controllers import ResetPasswordController

reset_password_router = Blueprint("reset_password_router", __name__)


@reset_password_router.post("/short.me/auth/reset-password/request")
async def send_reset_password_email():
    data = request.json
    timestamp = request.timestamp
    email = data.get("email", "")
    return await ResetPasswordController.send_reset_password_email(email, timestamp)


@reset_password_router.get("/short.me/auth/reset-password/status/<string:token>")
async def user_reset_password_information(token):
    timestamp = request.timestamp
    return await ResetPasswordController.user_reset_password_information(
        token, timestamp
    )


@reset_password_router.get("/short.me/auth/reset-password/verify/<string:token>")
async def get_user_reset_password_verification(token):
    timestamp = request.timestamp
    return await ResetPasswordController.get_user_reset_password_verification(
        token, timestamp
    )


@reset_password_router.patch("/short.me/auth/reset-password/confirm/<string:token>")
async def user_reset_password_verification(token):
    timestamp = request.timestamp
    json = request.json
    password = json.get("confirm_password", "")
    new_password = json.get("new_password", "")
    return await ResetPasswordController.user_reset_password_verification(
        token, password, new_password, timestamp
    )
