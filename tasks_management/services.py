from datetime import date

from core.services import BaseService
from tasks_management.models import Task
from tasks_management.validation import TaskValidation


class TaskService(BaseService):
    OBJECT_TYPE = Task

    def __init__(self, user, validation_class=TaskValidation):
        super().__init__(user, validation_class)

    def _base_payload_adjust(self, obj_data):
        data = obj_data.pop('data', None)
        if isinstance(data, dict):
            self._convert_dates_to_strings(data)
        return {**obj_data, "data": data}

    def _convert_dates_to_strings(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, date):
                dictionary[key] = value.isoformat()


class TasksManagementService(TaskService):
    def create_task(self, source, data, complete_action):
        task = self.create(obj_data={"source": source, "data": data, "complete_action": complete_action})
        return task

    def resolve_task(self):
        pass

    def assign_task_to_users(self):
        pass

    def send_business_status_change_signal(self):
        pass

    def send_business_status_complete_signal(self):
        pass