import mongoengine as me


class UserModel(me.Document):
    username = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    password = me.StringField(required=False)
    created_at = me.IntField(required=True)
    updated_at = me.IntField(required=True)
    provider = me.StringField(required=True)
    is_active = me.BooleanField(required=False, default=False)

    meta = {"collection": "users"}

    async def unique_field(self):
        if self.username:
            self.username = self.username.lower()
        if self.email:
            self.email = self.email.lower()
