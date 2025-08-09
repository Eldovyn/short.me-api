import mongoengine as me
from .base import BaseDocument


class OtpAccountActiveModel(BaseDocument):
    otp = me.StringField(required=True)

    account_active = me.ReferenceField(
        "AccountActiveModel", reverse_delete_rule=me.CASCADE
    )

    meta = {"collection": "otp_account_active"}
