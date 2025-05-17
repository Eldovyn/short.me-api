from .. import PRIVATE_KEY
import jwt


class AuthJwt:
    @staticmethod
    async def generate_jwt(username, datetime):
        payload = {"sub": username, "iat": datetime}
        token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
        return token
