from dataclasses import dataclass


@dataclass
class AccessTokenSchema:
    access_token: str
    created_at: int
