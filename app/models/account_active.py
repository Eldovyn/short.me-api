import mongoengine as me


class AccountActiveModel(me.Document):
    token_email = me.StringField(required=True)
    token_web = me.StringField(required=True)
    created_at = me.IntField(required=True)
    updated_at = me.IntField(required=True)
    expired_at = me.IntField(required=True)

    user = me.ReferenceField("UserModel", reverse_delete_rule=me.CASCADE)

    meta = {"collection": "account_active"}
