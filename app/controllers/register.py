from ..databases import UserDatabase, AccountActiveDatabase
from flask import jsonify
from email_validator import validate_email
from google.auth.transport import requests
import requests
import re
from ..utils import TokenEmailAccountActive, TokenWebAccountActive, SendEmail, AuthJwt
import datetime
from ..config import provider as PROVIDER


class RegisterController:
    @staticmethod
    async def user_register(
        provider, token, username, email, password, confirm_password, timestamp
    ):
        from ..bcrypt import bcrypt

        access_token = None
        token_web = None

        try:
            created_at = int(timestamp.timestamp())
            errors = {}
            if not isinstance(provider, str):
                errors.setdefault("provider", []).append("MUST_TEXT")
            if not provider or (isinstance(provider, str) and provider.isspace()):
                errors.setdefault("provider", []).append("IS_REQUIRED")
            if provider not in PROVIDER.split(", "):
                errors.setdefault("provider", []).append("IS_INVALID")
            if provider == "google":
                if not isinstance(token, str):
                    errors.setdefault("token", []).append("MUST_TEXT")
                if not token or (isinstance(token, str) and token.isspace()):
                    errors.setdefault("token", []).append("IS_REQUIRED")
                if not errors:
                    url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}"
                    response = requests.get(url)
                    resp = response.json()
                    username = resp["name"]
                    email = resp["email"]
                    if user_data := await UserDatabase.get("by_email", email=email):
                        return (
                            jsonify(
                                {
                                    "errors": {"user": ["USER_ALREADY_EXISTS"]},
                                    "message": "the user already exists",
                                }
                            ),
                            409,
                        )
                    result = await UserDatabase.insert(
                        provider, username, email, None, created_at
                    )
                    access_token = await AuthJwt.generate_jwt(result.id, created_at)
            else:
                if not isinstance(username, str):
                    errors.setdefault("username", []).append("MUST_TEXT")
                if not username or (isinstance(username, str) and username.isspace()):
                    errors.setdefault("username", []).append("IS_REQUIRED")
                if not isinstance(email, str):
                    errors.setdefault("email", []).append("MUST_TEXT")
                if not email or (isinstance(email, str) and email.isspace()):
                    errors.setdefault("email", []).append("IS_REQUIRED")
                if not isinstance(password, str):
                    errors.setdefault("password", []).append("MUST_TEXT")
                if not password or (isinstance(password, str) and password.isspace()):
                    errors.setdefault("password", []).append("IS_REQUIRED")
                if not isinstance(confirm_password, str):
                    errors.setdefault("confirm_password", []).append("MUST_TEXT")
                if not confirm_password or (
                    isinstance(confirm_password, str) and confirm_password.isspace()
                ):
                    errors.setdefault("confirm_password", []).append("IS_REQUIRED")
                try:
                    valid = validate_email(email)
                    email = valid.email
                except:
                    errors.setdefault("email", []).append("IS_INVALID")
                if password != confirm_password:
                    errors.setdefault("password_match", []).append("PASSWORD_MISMATCH")
                else:
                    if len(password) < 8:
                        errors.setdefault("password_security", []).append("TOO_SHORT")
                    if not re.search(r"[A-Z]", password):
                        errors.setdefault("password_security", []).append("NO_CAPITAL")
                    if not re.search(r"[a-z]", password):
                        errors.setdefault("password_security", []).append(
                            "NO_LOWERCASE"
                        )
                    if not re.search(r"[0-9]", password):
                        errors.setdefault("password_security", []).append("NO_NUMBER")
                    if not re.search(
                        r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password
                    ):
                        errors.setdefault("password_security", []).append("NO_SYMBOL")
                if errors:
                    return jsonify({"errors": errors, "message": "invalid data"}), 400
                result_password = bcrypt.generate_password_hash(password).decode(
                    "utf-8"
                )
                if user_data := await UserDatabase.get("by_email", email=email):
                    return (
                        jsonify(
                            {
                                "errors": {"user": ["ALREADY_EXISTS"]},
                                "message": "the user already exists",
                            }
                        ),
                        409,
                    )
            if provider != "google":
                result = await UserDatabase.insert(
                    provider, username, email, result_password, created_at
                )
                expired_at = timestamp + datetime.timedelta(minutes=5)
                token_web = await TokenWebAccountActive.insert(
                    f"{result.id}", int(timestamp.timestamp())
                )
                token_email = await TokenEmailAccountActive.insert(
                    f"{result.id}", int(timestamp.timestamp())
                )
                await AccountActiveDatabase.insert(
                    email,
                    token_web,
                    token_email,
                    int(timestamp.timestamp()),
                    int(expired_at.timestamp()),
                )
                SendEmail.send_email_verification(result, token_email)
            return (
                jsonify(
                    {
                        "message": "user registered successfully",
                        "data": {
                            "id": result.id,
                            "username": result.username,
                            "created_at": result.created_at,
                            "updated_at": result.updated_at,
                            "is_active": result.is_active,
                            "provider": result.provider,
                        },
                        "token": {
                            "access_token": access_token,
                            "token_web": token_web,
                        },
                    }
                ),
                201,
            )
        except Exception:
            return jsonify({"message": "invalid request"}), 400
