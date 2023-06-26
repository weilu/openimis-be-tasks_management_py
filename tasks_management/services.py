from datetime import date
from typing import Union, Dict
from uuid import UUID

from core.services import BaseService
from core.signals import register_service_signal

from .models import Task
from .validation import TaskValidation


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

            #TODO send signal
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


class TasksManagementService(TaskService):
    def create_task(self, source, data, executor_action_event):
        task = self.create(obj_data={"source": source, "data": data, "executor_action_event": executor_action_event})
        return task

    def resolve_task(self):
        pass

    def assign_task_to_users(self):
        pass

    def send_business_status_change_signal(self):
        pass

    def send_business_status_complete_signal(self):
        pass
