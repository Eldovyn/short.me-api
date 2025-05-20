from .database import Database
from ..models import AccountActiveModel, UserModel


class AccountActiveDatabase(Database):
    @staticmethod
    async def insert(email, token_web, token_email, created_at, expired_at):
        if data_user := UserModel.objects(email=email.lower()).first():
            if data_account_active := AccountActiveModel.objects(
                user=data_user
            ).first():
                data_account_active.token_web = token_web
                data_account_active.token_email = token_email
                data_account_active.updated_at = int(created_at)
                data_account_active.expired_at = int(expired_at)
                data_account_active.save()
                return data_account_active
            account_active_data = AccountActiveModel(
                user=data_user,
                token_web=token_web,
                token_email=token_email,
                created_at=int(created_at),
                updated_at=int(created_at),
                expired_at=int(expired_at),
            )
            account_active_data.save()
            return account_active_data

    @staticmethod
    async def get(category, **kwargs):
        token = kwargs.get("token")
        created_at = kwargs.get("created_at")
        if category == "by_token_web":
            if data_account_active := AccountActiveModel.objects(
                token_web=token
            ).first():
                if data_account_active.expired_at > int(created_at):
                    return data_account_active
                else:
                    data_account_active.user.save()
                    data_account_active.delete()
        if category == "by_token_email":
            if data_account_active := AccountActiveModel.objects(
                token_email=token
            ).first():
                if data_account_active.expired_at > int(created_at):
                    return data_account_active
                else:
                    data_account_active.user.save()
                    data_account_active.delete()

    @staticmethod
    async def delete(category, **kwargs):
        user_id = kwargs.get("user_id")
        if category == "user_active_by_token_email":
            if user_data := UserModel.objects(id=user_id).first():
                if data_account_active := AccountActiveModel.objects(
                    user=user_data
                ).first():
                    user_data.is_active = True
                    user_data.save()
                    data_account_active.delete()
                    return data_account_active

    @staticmethod
    async def update(category, **kwargs):
        pass
