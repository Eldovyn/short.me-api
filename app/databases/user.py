from .database import Database
from ..models import UserModel
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
        new_first_name = kwargs.get("new_first_name")
        new_last_name = kwargs.get("new_last_name")
        created_at = kwargs.get("created_at")
        new_username = kwargs.get("new_username")
        new_bio = kwargs.get("new_bio")
        new_country = kwargs.get("new_country")
        new_city = kwargs.get("new_city")
        if category == "first_name_by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.first_name = new_first_name
                user_data.updated_at = created_at
                user_data.save()
                return user_data
        if category == "last_name_by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.last_name = new_last_name
                user_data.updated_at = created_at
                user_data.save()
                return user_data
        if category == "username_by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.username = new_username
                user_data.updated_at = created_at
                user_data.save()
                return user_data
        if category == "bio_by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.bio = new_bio
                user_data.updated_at = created_at
                user_data.save()
                return user_data
        if category == "country_by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.country = new_country
                user_data.updated_at = created_at
                user_data.save()
                return user_data
        if category == "city_by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                user_data.city = new_city
                user_data.updated_at = created_at
                user_data.save()
                return user_data

    @staticmethod
    async def get(category, **kwargs):
        email = kwargs.get("email")
        username = kwargs.get("username")
        user_id = kwargs.get("user_id")
        if category == "by_email":
            if user_data := UserModel.objects(email=email.lower()).first():
                return user_data
        if category == "by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                return user_data
