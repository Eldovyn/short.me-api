from .database import Database
from ..models import AccountActiveModel, UserModel, OtpAccountActiveModel
from datetime import timezone


class AccountActiveDatabase(Database):
    @staticmethod
    async def insert(email, token_web, token_email, otp, expired_at):
        data_user = UserModel.objects(email=email.lower()).first()
        if not data_user:
            return None

        data_account_active = AccountActiveModel.objects(user=data_user).first()
        if not data_account_active:
            data_account_active = AccountActiveModel(
                user=data_user,
                token_web=token_web,
                token_email=token_email,
                expired_at=expired_at,
            )
        else:
            data_account_active.token_web = token_web
            data_account_active.token_email = token_email
            data_account_active.expired_at = expired_at
        data_account_active.save()

        data_otp = OtpAccountActiveModel.objects(
            account_active=data_account_active
        ).first()
        if data_otp:
            data_otp.otp = otp
        else:
            data_otp = OtpAccountActiveModel(
                account_active=data_account_active, otp=otp
            )
        data_otp.save()

        return data_otp

    @staticmethod
    async def get(category, **kwargs):
        token = kwargs.get("token")
        created_at = kwargs.get("created_at")
        otp = kwargs.get("otp")
        if category == "by_token_web":
            if data_account_active := AccountActiveModel.objects(
                token_web=token
            ).first():
                if (
                    data_account_active.expired_at.replace(tzinfo=timezone.utc)
                    > created_at
                ):
                    return data_account_active
                else:
                    data_account_active.user.save()
                    data_account_active.delete()
        if category == "by_token_email":
            if data_account_active := AccountActiveModel.objects(
                token_email=token
            ).first():
                if (
                    data_account_active.expired_at.replace(tzinfo=timezone.utc)
                    > created_at
                ):
                    return data_account_active
                else:
                    data_account_active.user.save()
                    data_account_active.delete()
        if category == "by_token_email_otp":
            if data_account_active := AccountActiveModel.objects(
                token_email=token
            ).first():
                if data_otp := OtpAccountActiveModel.objects(
                    account_active=data_account_active, otp=otp
                ).first():
                    if (
                        data_account_active.expired_at.replace(tzinfo=timezone.utc)
                        > created_at
                    ):
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
        if category == "by_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                if data_account_active := AccountActiveModel.objects(
                    user=user_data
                ).first():
                    data_account_active.delete()
                    return data_account_active

    @staticmethod
    async def update(category, **kwargs):
        pass
