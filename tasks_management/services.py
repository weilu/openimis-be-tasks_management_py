import logging
from typing import Type, Dict

from django.db import transaction

from core.services import create_or_update_core_user, BaseService
from core.services.utils import check_authentication, output_exception, model_representation, output_result_success
from tasks_management.models import TaskGroup, TaskExecutor
from tasks_management.validation import TaskGroupValidation, TaskExecutorValidation

logger = logging.getLogger(__name__)


class TaskGroupService(BaseService):
    OBJECT_TYPE: Type[TaskGroup] = TaskGroup

    def __init__(self, user, validation_class=TaskGroupValidation):
        super().__init__(user, validation_class)

    @check_authentication
    @transaction.atomic
    def create(self, obj_data: Dict[str, any]):
        try:
            with transaction.atomic():
                user_ids = obj_data.pop('user_ids')
                self.validation_class.validate_create(self.user, **obj_data)
                obj_: TaskGroup = self.OBJECT_TYPE(**obj_data)
                task_group_output = self.save_instance(obj_)
                task_group_id = task_group_output['data']['id']
                task_executor_service = TaskExecutorService(self.user)
                # TODO: it would be good to override bulk_create and use it here
                for user_id in user_ids:
                    task_executor_service.create({
                        "task_group_id": task_group_id,
                        "user_id": user_id
                    })
                return task_group_output
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create", exception=exc)

    @check_authentication
    def update(self, obj_data):
        user_ids = obj_data.pop('user_ids')
        task_group_id = obj_data.get('id')
        task_group = TaskGroup.objects.get(id=task_group_id)
        current_task_executors = task_group.taskexecutor_set.filter(is_deleted=False)
        current_user_ids = current_task_executors.values_list('user__id', flat=True)
        if set(current_user_ids) != set(user_ids):
            self._update_task_group_task_executors(task_group, user_ids)
        return super().update(obj_data)

    @transaction.atomic
    def _update_task_group_task_executors(self, task_group, user_ids):
        try:
            task_group.taskexecutor_set.all().delete()
            service = TaskExecutorService(self.user)
            for user_id in user_ids:
                service.create({'task_group_id': task_group.id,
                                'user_id': user_id})
        except Exception as exc:
            raise exc

    def delete(self, obj_data: Dict[str, any]):
        id = obj_data.get("id")
        if id:
            task_group = TaskGroup.objects.filter(id=id).first()
            task_group.taskexecutor_set.all().delete()
        return super().delete(obj_data)


class TaskExecutorService(BaseService):
    OBJECT_TYPE: Type[TaskExecutor] = TaskExecutor

    def __init__(self, user, validation_class=TaskExecutorValidation):
        super().__init__(user, validation_class)
