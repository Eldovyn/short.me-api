from flask import Blueprint, request
from ..controllers import AccountActiveController

account_active_router = Blueprint("account_active_router", __name__)


@account_active_router.post("/short.me/auth/account-active/request")
async def send_account_active_email():
    data = request.json
    timestamp = request.timestamp
    email = data.get("email", "")
    return await AccountActiveController.send_account_active_email(email, timestamp)


@account_active_router.get("/short.me/auth/account-active/status/<string:token>")
async def user_account_active_information(token):
    timestamp = request.timestamp
    return await AccountActiveController.user_account_active_information(
        token, timestamp
    )


@account_active_router.get("/short.me/auth/account-active/verify/<string:token>")
async def get_user_account_active_verification(token):
    timestamp = request.timestamp
    return await AccountActiveController.get_user_account_active_verification(
        token, timestamp
    )


@account_active_router.patch("/short.me/auth/account-active/active/<string:token>")
async def user_account_active_verification(token):
    timestamp = request.timestamp
    return await AccountActiveController.user_account_active_verification(
        token, timestamp
    )
