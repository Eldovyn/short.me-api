from .database import Database
from ..models import UserModel, OtpEmailModel
import mongoengine as me


class UserDatabase(Database):
    @staticmethod
    async def insert(provider, username, email, password, created_at):
        user_data = UserModel(
            username=username,
            email=email,
            password=password,
            created_at=int(created_at),
            updated_at=int(created_at),
            provider=provider,
        )
        if provider == "google":
            user_data.is_active = True
        await user_data.unique_field()
        user_data.save()
        return user_data

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        user_id = kwargs.get("user_id")
        username = kwargs.get("username")
        password = kwargs.get("password")
        email = kwargs.get("email")
        created_at = kwargs.get("created_at")
        otp = kwargs.get("otp")
        if category == "username":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.username = username
                user_data.save()
                return user_data
        if category == "password":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.password = password
                user_data.updated_at = created_at
                user_data.save()
                return user_data
        if category == "email":
            if user_data := UserModel.objects(id=user_id).first():
                if data_otp := OtpEmailModel.objects(user=user_data, otp=otp).first():
                    user_data.email = email
                    user_data.updated_at = created_at
                    user_data.save()
                    data_otp.delete()
                    return data_otp

    @staticmethod
    async def get(category, **kwargs):
        email = kwargs.get("email")
        user_id = kwargs.get("user_id")
        if category == "by_email":
            if user_data := UserModel.objects(email=email.lower()).first():
                return user_data
        if category == "by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                return user_data
