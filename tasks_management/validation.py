from core.validation import BaseModelValidation
from tasks_management.models import Task


class TaskValidation(BaseModelValidation):
    OBJECT_TYPE = Task
