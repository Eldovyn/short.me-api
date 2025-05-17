from flask import Blueprint, request
from ..controllers import LoginController

login_router = Blueprint("login_router", __name__)


@login_router.post("/short.me/login")
async def user_login():
    data = request.json
    timestamp = request.timestamp
    email = data.get("email", "")
    password = data.get("password", "")
    provider = data.get("provider", "")
    token = data.get("token", "")
    return await LoginController.user_login(provider, token, email, password, timestamp)
