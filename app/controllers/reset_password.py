from ..databases import UserDatabase, ResetPasswordDatabase
from flask import jsonify
from email_validator import validate_email
from ..utils import TokenWebResetPassword, TokenEmailResetPassword, SendEmail
import datetime
import re


class ResetPasswordController:
    @staticmethod
    async def get_user_reset_password_verification(token, timestamp):
        created_at = int(timestamp.timestamp())
        errors = {}
        if not isinstance(token, str):
            errors.setdefault("token", []).append("MUST_TEXT")
        if not token or (isinstance(token, str) and token.isspace()):
            errors.setdefault("token", []).append("IS_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (
            user_data := await ResetPasswordDatabase.get(
                "by_token_email", token=token, created_at=created_at
            )
        ):
            return (
                jsonify(
                    {
                        "errors": {"token": ["IS_INVALID"]},
                        "message": "user not found",
                    }
                ),
                404,
            )
        return (
            jsonify(
                {
                    "message": "successfully get reset password information",
                    "data": {
                        "id": user_data.id,
                        "token_web": user_data.token_web,
                        "created_at": user_data.created_at,
                        "updated_at": user_data.updated_at,
                        "expired_at": user_data.expired_at,
                    },
                    "user": {
                        "id": user_data.user.id,
                        "username": user_data.user.username,
                        "created_at": user_data.user.created_at,
                        "updated_at": user_data.user.updated_at,
                        "is_active": user_data.user.is_active,
                        "provider": user_data.user.provider,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def user_reset_password_verification(
        token, new_password, confirm_password, timestamp
    ):
        from ..bcrypt import bcrypt

        created_at = int(timestamp.timestamp())
        errors = {}
        if not isinstance(token, str):
            errors.setdefault("token", []).append("MUST_TEXT")
        if not token or (isinstance(token, str) and token.isspace()):
            errors.setdefault("token", []).append("IS_REQUIRED")
        if not isinstance(new_password, str):
            errors.setdefault("new_password", []).append("MUST_TEXT")
        if not new_password or (
            isinstance(new_password, str) and new_password.isspace()
        ):
            errors.setdefault("password", []).append("IS_REQUIRED")
        if not isinstance(confirm_password, str):
            errors.setdefault("confirm_password", []).append("MUST_TEXT")
        if not confirm_password or (
            isinstance(confirm_password, str) and confirm_password.isspace()
        ):
            errors.setdefault("confirm_password", []).append("IS_REQUIRED")
        if new_password != confirm_password:
            errors.setdefault("password_match", []).append("PASSWORD_MISMATCH")
        if len(new_password) < 8:
            errors.setdefault("password_security", []).append("TOO_SHORT")
        if not re.search(r"[A-Z]", new_password):
            errors.setdefault("password_security", []).append("NO_CAPITAL")
        if not re.search(r"[a-z]", new_password):
            errors.setdefault("password_security", []).append("NO_LOWERCASE")
        if not re.search(r"[0-9]", new_password):
            errors.setdefault("password_security", []).append("NO_NUMBER")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", new_password):
            errors.setdefault("password_security", []).append("NO_SYMBOL")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        result_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (
            user_data := await ResetPasswordDatabase.get(
                "by_token_email", token=token, created_at=created_at
            )
        ):
            return (
                jsonify(
                    {
                        "errors": {"token": ["IS_INVALID"]},
                        "message": "user not found",
                    }
                ),
                404,
            )
        token_web = await TokenEmailResetPassword.get(token)
        await ResetPasswordDatabase.delete(
            "user_password_by_token_email",
            token=user_data.token_email,
            user_id=token_web["user_id"],
            new_password=result_password,
            created_at=created_at,
        )
        return (
            jsonify(
                {
                    "message": "successfully verify user account",
                    "data": {
                        "id": user_data.id,
                        "token_web": user_data.token_web,
                        "created_at": user_data.created_at,
                        "updated_at": user_data.updated_at,
                        "expired_at": user_data.expired_at,
                    },
                    "user": {
                        "id": user_data.user.id,
                        "username": user_data.user.username,
                        "created_at": user_data.user.created_at,
                        "updated_at": user_data.user.updated_at,
                        "is_active": user_data.user.is_active,
                        "provider": user_data.user.provider,
                        "email": user_data.user.email,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def user_reset_password_information(token, timestamp):
        created_at = int(timestamp.timestamp())
        errors = {}
        if not isinstance(token, str):
            errors.setdefault("token", []).append("MUST_TEXT")
        if not token or (isinstance(token, str) and token.isspace()):
            errors.setdefault("token", []).append("IS_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (
            user_data := await ResetPasswordDatabase.get(
                "by_token_web", token=token, created_at=created_at
            )
        ):
            return (
                jsonify(
                    {
                        "errors": {"token": ["IS_INVALID"]},
                        "message": "user not found",
                    }
                ),
                404,
            )
        return (
            jsonify(
                {
                    "message": "successfully get reset password information",
                    "data": {
                        "id": user_data.id,
                        "token_web": user_data.token_web,
                        "created_at": user_data.created_at,
                        "updated_at": user_data.updated_at,
                        "expired_at": user_data.expired_at,
                    },
                    "user": {
                        "id": user_data.user.id,
                        "email": user_data.user.email,
                        "username": user_data.user.username,
                        "created_at": user_data.user.created_at,
                        "updated_at": user_data.user.updated_at,
                        "is_active": user_data.user.is_active,
                        "provider": user_data.user.provider,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def send_reset_password_email(email, timestamp):
        errors = {}
        if not isinstance(email, str):
            errors.setdefault("email", []).append("MUST_TEXT")
        if not email or (isinstance(email, str) and email.isspace()):
            errors.setdefault("email", []).append("IS_REQUIRED")
        try:
            valid = validate_email(email)
            email = valid.email
        except:
            errors.setdefault("email", []).append("IS_INVALID")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (user_data := await UserDatabase.get("by_email", email=email)):
            return (
                jsonify(
                    {"errors": {"user": ["NOT_FOUND"]}, "message": "email not found"}
                ),
                404,
            )
        if user_data.provider != "auth_internal":
            return (
                jsonify(
                    {
                        "errors": {"user": ["NOT_FOUND"]},
                        "message": "email not found",
                    }
                ),
                404,
            )
        expired_at = timestamp + datetime.timedelta(minutes=5)
        token_web = await TokenWebResetPassword.insert(
            f"{user_data.id}", int(timestamp.timestamp())
        )
        token_email = await TokenEmailResetPassword.insert(
            f"{user_data.id}", int(timestamp.timestamp())
        )
        reset_password_data = await ResetPasswordDatabase.insert(
            email,
            token_web,
            token_email,
            int(timestamp.timestamp()),
            int(expired_at.timestamp()),
        )
        SendEmail.send_email_reset_password(user_data, token_email)
        return (
            jsonify(
                {
                    "message": "successfully send reset password email",
                    "data": {
                        "id": reset_password_data.id,
                        "token_web": reset_password_data.token_web,
                        "created_at": reset_password_data.created_at,
                        "updated_at": reset_password_data.updated_at,
                        "expired_at": reset_password_data.expired_at,
                    },
                    "user": {
                        "id": reset_password_data.user.id,
                        "username": reset_password_data.user.username,
                        "created_at": reset_password_data.user.created_at,
                        "updated_at": reset_password_data.user.updated_at,
                        "is_active": reset_password_data.user.is_active,
                        "provider": reset_password_data.user.provider,
                    },
                }
            ),
            201,
        )
