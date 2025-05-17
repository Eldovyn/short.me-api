from flask import Blueprint, request
from ..controllers import RegisterController

register_router = Blueprint("register_router", __name__)


@register_router.post("/short.me/register")
async def user_register():
    data = request.json
    timestamp = request.timestamp
    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    provider = data.get("provider", "")
    token = data.get("token", "")
    return await RegisterController.user_register(
        provider, token, username, email, password, confirm_password, timestamp
    )
