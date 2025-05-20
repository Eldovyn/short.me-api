from ..databases import OtpEmailDatabase
from ..utils import SendEmail
from flask import jsonify
import string
import datetime
import random


class OtpController:
    @staticmethod
    async def otp_email(user, timestamp):
        karakter = string.ascii_uppercase + string.digits
        expired_at = timestamp + datetime.timedelta(minutes=5)
        otp = "".join(random.choices(karakter, k=6))
        if not (
            data_otp := await OtpEmailDatabase.insert(
                user.id, otp, int(timestamp.timestamp()), int(expired_at.timestamp())
            )
        ):
            return (
                jsonify(
                    {
                        "message": "invalid or expired token",
                        "errors": {"token": ["IS_INVALID"]},
                    }
                ),
                401,
            )
        SendEmail.send_email_otp(user, otp)
        return jsonify({"message": "successfully send otp"}), 201
