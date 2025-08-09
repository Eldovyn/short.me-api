from .. import celery_app
from ..models import UserModel
from celery.result import AsyncResult


@celery_app.task(name="deleted_account_task")
def deleted_account_task(user_id):
    if data_user := UserModel.objects(id=user_id).first():
        data_user.is_deleted = True
        data_user.save()
    return f"deleted account {user_id}"


def cancle_deleted_account(task_id):
    task = AsyncResult(task_id, app=celery_app)
    task.revoke(terminate=True)
