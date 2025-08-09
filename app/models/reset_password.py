import mongoengine as me
from .base import BaseDocument


class ResetPasswordModel(BaseDocument):
    token_email = me.StringField(required=True)
    token_web = me.StringField(required=True)
    expired_at = me.DateTimeField(required=True)

    user = me.ReferenceField("UserModel", reverse_delete_rule=me.CASCADE)

    meta = {"collection": "reset_password"}
