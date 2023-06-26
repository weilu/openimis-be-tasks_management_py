from core.validation import BaseModelValidation

from .models import Task


class TaskValidation(BaseModelValidation):
    OBJECT_TYPE = Task
