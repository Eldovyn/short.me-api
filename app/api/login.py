from flask import Blueprint, request
from ..controllers import LoginController
from ..utils import jwt_required

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


@login_router.post("/short.me/logout")
@jwt_required()
async def user_logout():
    user = request.user
    token = request.token
    return await LoginController.user_logout(user, token)
