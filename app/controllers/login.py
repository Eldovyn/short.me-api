from ..databases import UserDatabase, AccountActiveDatabase, BlacklistTokenDatabase
from flask import jsonify
from email_validator import validate_email
from google.auth.transport import requests
import requests
from ..utils import AuthJwt, TokenEmailAccountActive, TokenWebAccountActive, SendEmail
import datetime
from ..config import provider as PROVIDER


class LoginController:
    @staticmethod
    async def user_logout(user, token):
        if not (
            user_token := await BlacklistTokenDatabase.insert(user.id, token["iat"])
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
        return jsonify({"message": "successfully logout"}), 201

    @staticmethod
    async def user_login(provider, token, email, password, timestamp):
        from ..bcrypt import bcrypt

        token_web = None
        access_token = None

        try:
            errors = {}
            if not isinstance(provider, str):
                errors.setdefault("provider", []).append("MUST_TEXT")
            if not provider or (isinstance(provider, str) and provider.isspace()):
                errors.setdefault("provider", []).append("IS_REQUIRED")
            if provider not in PROVIDER.split(", "):
                errors.setdefault("provider", []).append("IS_INVALID")

            if provider == "google":
                if not errors:
                    url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}"
                    response = requests.get(url)
                    resp = response.json()
                    email = resp["email"]
                    if not (
                        user_data := await UserDatabase.get("by_email", email=email)
                    ):
                        return (
                            jsonify(
                                {
                                    "errors": {"user": ["NOT_FOUND"]},
                                    "message": "you are not registered",
                                }
                            ),
                            401,
                        )
                    if not user_data.is_active:
                        return (
                            jsonify(
                                {
                                    "errors": {"user": ["NOT_ACTIVE"]},
                                    "message": "user is not active",
                                }
                            ),
                            401,
                        )
                    if not user_data.provider == "google":
                        return (
                            jsonify(
                                {
                                    "errors": {"user": ["NOT_FOUND"]},
                                    "message": "you are not registered",
                                }
                            ),
                            401,
                        )
                    access_token = await AuthJwt.generate_jwt(
                        f"{user_data.id}", int(timestamp.timestamp())
                    )
            else:
                if not isinstance(email, str):
                    errors.setdefault("email", []).append("MUST_TEXT")
                if not email or (isinstance(email, str) and email.isspace()):
                    errors.setdefault("email", []).append("IS_REQUIRED")
                if not isinstance(password, str):
                    errors.setdefault("password", []).append("MUST_TEXT")
                if not password or (isinstance(password, str) and password.isspace()):
                    errors.setdefault("password", []).append("IS_REQUIRED")
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
                            {
                                "errors": {"user": ["NOT_FOUND"]},
                                "message": "invalid email or password",
                            }
                        ),
                        401,
                    )
                if not bcrypt.check_password_hash(user_data.password, password):
                    return (
                        jsonify(
                            {
                                "errors": {"user": ["NOT_FOUND"]},
                                "message": "invalid email or password",
                            }
                        ),
                        401,
                    )
                if not user_data.is_active:
                    expired_at = timestamp + datetime.timedelta(minutes=5)
                    token_web = await TokenWebAccountActive.insert(
                        f"{user_data.id}", int(timestamp.timestamp())
                    )
                    token_email = await TokenEmailAccountActive.insert(
                        f"{user_data.id}", int(timestamp.timestamp())
                    )
                    await AccountActiveDatabase.insert(
                        email,
                        token_web,
                        token_email,
                        int(timestamp.timestamp()),
                        int(expired_at.timestamp()),
                    )
                    SendEmail.send_email_verification(user_data, token_email)
                    return (
                        jsonify(
                            {
                                "message": "user not active",
                                "data": {
                                    "id": user_data.id,
                                    "username": user_data.username,
                                    "created_at": user_data.created_at,
                                    "updated_at": user_data.updated_at,
                                    "is_active": user_data.is_active,
                                    "provider": user_data.provider,
                                    "email": user_data.email,
                                },
                                "token": {
                                    "access_token": None,
                                    "token_web": token_web,
                                },
                            }
                        ),
                        403,
                    )
                access_token = await AuthJwt.generate_jwt(
                    f"{user_data.id}", int(timestamp.timestamp())
                )
            return (
                jsonify(
                    {
                        "message": "user login successfully",
                        "data": {
                            "id": user_data.id,
                            "username": user_data.username,
                            "created_at": user_data.created_at,
                            "updated_at": user_data.updated_at,
                            "is_active": user_data.is_active,
                            "provider": user_data.provider,
                        },
                        "token": {"access_token": access_token, "token_web": token_web},
                    }
                ),
                201,
            )
        except Exception:
            return jsonify({"message": "invalid request"}), 400
