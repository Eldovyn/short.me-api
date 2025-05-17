from flask import Blueprint, request
from ..controllers import AccountActiveController

account_active_router = Blueprint("account_active_router", __name__)


@account_active_router.post("/short.me/account-active")
async def send_account_active_email():
    data = request.json
    timestamp = request.timestamp
    email = data.get("email", "")
    return await AccountActiveController.send_account_active_email(email, timestamp)


@account_active_router.get("/short.me/account-active/email-verification")
async def user_account_active_information():
    data = request.args
    timestamp = request.timestamp
    token = data.get("token", "")
    return await AccountActiveController.user_account_active_information(
        token, timestamp
    )


@account_active_router.patch("/short.me/account-active/verification/email-verification")
async def user_account_active_verification():
    json = request.json
    timestamp = request.timestamp
    token = json.get("token", "")
    return await AccountActiveController.user_account_active_verification(
        token, timestamp
    )


@account_active_router.get("/short.me/account-active/verification/email-verification")
async def get_user_account_active_verification():
    data = request.args
    timestamp = request.timestamp
    token = data.get("token", "")
    return await AccountActiveController.get_user_account_active_verification(
        token, timestamp
    )
