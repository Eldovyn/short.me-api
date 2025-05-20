from flask import Blueprint, request
from ..controllers import OtpController
from ..utils import jwt_required

otp_router = Blueprint("otp_router", __name__)


@otp_router.post("/short.me/otp/email")
@jwt_required()
async def user_login():
    user = request.user
    timestamp = request.timestamp
    return await OtpController.otp_email(user, timestamp)
