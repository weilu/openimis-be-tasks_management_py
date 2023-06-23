import logging

from django.db import transaction

from core.services import create_or_update_core_user, BaseService
from core.services.utils import check_authentication, output_exception, model_representation, output_result_success
from tasks_management.models import TaskGroup, TaskExecutor
from tasks_management.validation import TaskGroupValidation, TaskExecutorValidation

logger = logging.getLogger(__name__)


class TaskGroupService:
    OBJECT_TYPE = TaskGroup

    def __init__(self, user):
        self.user = user
        self.validation_class = TaskGroupValidation

    @check_authentication
    def create(self, obj_data):
        try:
            with transaction.atomic():
                user_ids = obj_data.pop('user_ids')
                self.validation_class.validate_create(self.user, **obj_data)
                obj_ = self.OBJECT_TYPE(**obj_data)
                task_group_output = self.save_instance(obj_)
                task_group_id = task_group_output['data']['id']
                task_executor_service = TaskExecutorService(self.user)
                for user_id in user_ids:
                    task_executor_service.create({
                        "task_group_id": task_group_id,
                        "user_id": user_id
                    })
                return task_group_output
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create", exception=exc)

    def save_instance(self, obj_):
        obj_.save(username=self.user.username)
        dict_repr = model_representation(obj_)
        return output_result_success(dict_representation=dict_repr)


class TaskExecutorService(BaseService):
    OBJECT_TYPE = TaskExecutor

    def __init__(self, user, validation_class=TaskExecutorValidation):
        super().__init__(user, validation_class)
