from .. import PRIVATE_KEY
import jwt


class AuthJwt:
    @staticmethod
    async def generate_jwt(user_id, datetime):
        payload = {"sub": user_id, "iat": datetime}
        token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
        return token
