import logging
from datetime import date
from typing import Union, Dict, Type
from uuid import UUID

from django.db import transaction

from core.services import BaseService
from core.signals import register_service_signal
from core.services.utils import check_authentication, output_exception

from tasks_management.models import TaskGroup, TaskExecutor, Task
from tasks_management.validation import TaskGroupValidation, TaskExecutorValidation, TaskValidation

logger = logging.getLogger(__name__)


class TaskService(BaseService):
    OBJECT_TYPE = Task

    def __init__(self, user, validation_class=TaskValidation):
        super().__init__(user, validation_class)

    @register_service_signal('task_service.create')
    def create(self, obj_data):
        return super().create(obj_data)

    @register_service_signal('task_service.update')
    def update(self, obj_data):
        return super().update(obj_data)

    @register_service_signal('task_service.delete')
    def delete(self, obj_data):
        return super().delete(obj_data)

    def complete_task(self, uuid: Union[str, UUID], success: bool, data: Dict):
        obj = self.OBJECT_TYPE.objects.filter(id=uuid).first()
        if not obj:
            return self._result(False, None, 'Task not found', str(uuid))
        if not obj.status == self.OBJECT_TYPE.Status.ACCEPTED:
            return self._result(False, None, 'Task not in `ACCEPTED` status', str(uuid))
        if success:
            obj.status = self.OBJECT_TYPE.Status.COMPLETED

            # TODO send signal
        else:
            obj.status = self.OBJECT_TYPE.Status.FAILED

        obj.save(username=self.user.login_name)
        return self._result(success)

    def _base_payload_adjust(self, obj_data):
        data = obj_data.pop('data', None)
        if isinstance(data, dict):
            self._convert_dates_to_strings(data)
        return {**obj_data, "data": data}

    def _convert_dates_to_strings(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, date):
                dictionary[key] = value.isoformat()

    def _result(self, success, data=None, message='', details=''):
        if data is None:
            data = dict()
        result = {'success': success}
        if success:
            result['data'] = data
        else:
            result['message'] = message
            result['details'] = details
        return result


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
    def update(self, obj_data: Dict[str, any]):
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
