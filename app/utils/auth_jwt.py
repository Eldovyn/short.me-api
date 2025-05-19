from .. import PRIVATE_KEY, PUBLIC_KEY
import jwt


class AuthJwt:
    @staticmethod
    async def generate_jwt(user_id, datetime):
        payload = {"sub": user_id, "iat": datetime}
        token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
        return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
