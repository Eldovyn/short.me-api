from .token import Token
from itsdangerous.url_safe import URLSafeSerializer
from ..config import salt_reset_password_email, secret_key_reset_password_email


class TokenEmailResetPassword(Token):
    @staticmethod
    async def insert(user_id, created_at):
        s = URLSafeSerializer(
            secret_key_reset_password_email, salt=salt_reset_password_email
        )
        token = s.dumps({"user_id": user_id, "created_at": created_at})
        return token

    @staticmethod
    async def get(token):
        s = URLSafeSerializer(
            secret_key_reset_password_email, salt=salt_reset_password_email
        )
        try:
            s.loads(token)["user_id"]
            s.loads(token)["created_at"]
        except:
            return None
        else:
            return s.loads(token)
