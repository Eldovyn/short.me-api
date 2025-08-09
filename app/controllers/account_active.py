from ..databases import UserDatabase, AccountActiveDatabase
from flask import jsonify, request, make_response
from ..utils import (
    TokenWebAccountActive,
    TokenEmailAccountActive,
    SendEmail,
    Validation,
    generate_etag,
    generate_otp,
)
import datetime
import string
import random
from ..serializers import UserSerializer, TokenSerializer
from ..config import web_short_me


class AccountActiveController:
    def __init__(self):
        self.user_seliazer = UserSerializer()
        self.token_serializer = TokenSerializer()

    async def get_user_account_active_verification(self, token, timestamp):
        errors = {}
        await Validation.validate_token(errors, token, "email_token_account_active")
        if errors:
            return jsonify({"errors": errors, "message": "validation errors"}), 400
        if not (
            user_token := await AccountActiveDatabase.get(
                "by_token_email", token=token, created_at=timestamp
            )
        ):
            return (
                jsonify(
                    {
                        "message": "validation errors",
                        "errors": {"token": ["IS_INVALID"]},
                    }
                ),
                422,
            )
        current_user = self.user_seliazer.serialize(user_token.user)
        token_data = self.token_serializer.serialize(user_token)
        combined_data = {**current_user, **token_data}
        etag = generate_etag(combined_data)

        client_etag = request.headers.get("If-None-Match")
        if client_etag == etag:
            return make_response("", 304)

        response_data = {
            "message": "successfully get account active information",
            "data": token_data,
            "user": current_user,
        }

        response = make_response(jsonify(response_data), 200)
        response.headers["Content-Type"] = "application/json"
        response.headers["ETag"] = etag
        return response

    async def user_account_active_verification_re_send(self, token, timestamp):
        errors = {}
        await Validation.validate_token(errors, token, "email_token_account_active")
        if errors:
            return jsonify({"errors": errors, "message": "validation errors"}), 400
        if not (
            user_token := await AccountActiveDatabase.get(
                "by_token_email", token=token, created_at=timestamp
            )
        ):
            errors.setdefault("token", []).append("IS_INVALID")
        if errors:
            return (
                jsonify({"message": "validation errors", "errors": errors}),
                422,
            )
        expired_at = timestamp + datetime.timedelta(minutes=5)
        token_web = await TokenWebAccountActive.insert(
            f"{user_token.user.id}", int(timestamp.timestamp())
        )
        token_email = await TokenEmailAccountActive.insert(
            f"{user_token.id}", int(timestamp.timestamp())
        )
        otp = generate_otp(4)
        account_active_data = await AccountActiveDatabase.insert(
            user_token.user.email, token_web, token_email, otp, expired_at
        )
        SendEmail.send_email(
            "Verification Your Account",
            [user_token.user.email],
            f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Active</title>
</head>
<body>
    <p>Hello {user_token.user.username},</p>
    <p>Someone has requested a link to verify your account, and you can do this through the link below.</p>
    <p>your otp is {otp}.</p>
    <p>
        <a href="{web_short_me}/account-active?token={token_email}">
            Click here to activate your account
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
                """,
        )
        user_me = self.user_seliazer.serialize(account_active_data.account_active.user)
        token_data = self.token_serializer.serialize(
            account_active_data.account_active, token_email_is_null=True
        )
        return (
            jsonify(
                {
                    "message": "successfully send account active email",
                    "data": token_data,
                    "user": user_me,
                }
            ),
            201,
        )

    async def user_account_active_verification(self, token, otp, timestamp):
        errors = {}
        await Validation.validate_token(errors, token, "email_token_account_active")
        await Validation.validate_otp(errors, otp)
        if errors:
            return jsonify({"errors": errors, "message": "validation errors"}), 400
        if not (
            user_token := await AccountActiveDatabase.get(
                "by_token_email", token=token, created_at=timestamp
            )
        ):
            errors.setdefault("token", []).append("IS_INVALID")
        if not (
            user_token := await AccountActiveDatabase.get(
                "by_token_email_otp", token=token, otp=otp, created_at=timestamp
            )
        ):
            errors.setdefault("otp", []).append("IS_INVALID")
        if errors:
            return (
                jsonify({"message": "validation errors", "errors": errors}),
                422,
            )
        await AccountActiveDatabase.delete(
            "user_active_by_token_email",
            token=user_token.token_email,
            user_id=user_token.user.id,
        )
        current_user = self.user_seliazer.serialize(user_token.user)
        token_data = self.token_serializer.serialize(user_token)
        return (
            jsonify(
                {
                    "message": "email verified successfully",
                    "data": token_data,
                    "user": current_user,
                }
            ),
            201,
        )

    async def user_account_active_information(self, token, timestamp):
        errors = {}
        await Validation.validate_token(errors, token, "web_token_account_active")
        await Validation.validate_required_text(errors, "token", token)
        if errors:
            return jsonify({"errors": errors, "message": "validation errors"}), 400
        if not (
            user_token := await AccountActiveDatabase.get(
                "by_token_web", token=token, created_at=timestamp
            )
        ):
            return (
                jsonify(
                    {
                        "message": "validation errors",
                        "errors": {"token": ["IS_INVALID"]},
                    }
                ),
                422,
            )
        current_user = self.user_seliazer.serialize(user_token.user)
        token_data = self.token_serializer.serialize(
            user_token, token_email_is_null=True
        )
        combined_data = {**current_user, **token_data}
        etag = generate_etag(combined_data)

        client_etag = request.headers.get("If-None-Match")
        if client_etag == etag:
            return make_response("", 304)

        response_data = {
            "message": "successfully get account active information",
            "data": token_data,
            "user": current_user,
        }

        response = make_response(jsonify(response_data), 200)
        response.headers["Content-Type"] = "application/json"
        response.headers["ETag"] = etag
        return response

    async def send_account_active_email(self, email, timestamp):
        errors = {}
        await Validation.validate_required_text(errors, "email", email)
        if errors:
            return jsonify({"errors": errors, "message": "validation errors"}), 400
        if not (user_data := await UserDatabase.get("by_email", email=email)):
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        if user_data.provider != "auth_internal":
            return (
                jsonify(
                    {
                        "message": "validation errors",
                        "errors": {"email": ["IS_INVALID"]},
                    }
                ),
                422,
            )
        if user_data.is_active:
            return (
                jsonify(
                    {
                        "message": "your account is active",
                    }
                ),
                409,
            )
        expired_at = timestamp + datetime.timedelta(minutes=5)
        token_web = await TokenWebAccountActive.insert(
            f"{user_data.id}", int(timestamp.timestamp())
        )
        token_email = await TokenEmailAccountActive.insert(
            f"{user_data.id}", int(timestamp.timestamp())
        )
        otp = generate_otp(4)
        account_active_data = await AccountActiveDatabase.insert(
            email, token_web, token_email, otp, expired_at
        )
        SendEmail.send_email(
            "Verification Your Account",
            [user_data.email],
            f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Active</title>
</head>
<body>
    <p>Hello {user_data.username},</p>
    <p>Someone has requested a link to verify your account, and you can do this through the link below.</p>
    <p>your otp is {otp}.</p>
    <p>
        <a href="{web_short_me}/account-active?token={token_email}">
            Click here to activate your account
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
                """,
        )
        user_me = self.user_seliazer.serialize(account_active_data.account_active.user)
        token_data = self.token_serializer.serialize(
            account_active_data.account_active, token_email_is_null=True
        )
        return (
            jsonify(
                {
                    "message": "successfully send account active email",
                    "data": token_data,
                    "user": user_me,
                }
            ),
            201,
        )
