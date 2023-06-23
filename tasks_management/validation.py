from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from core.validation import BaseModelValidation
from tasks_management.models import TaskGroup


class TaskGroupValidation(BaseModelValidation):
    OBJECT_TYPE = TaskGroup

    @classmethod
    def validate_create(cls, user, **data):
        errors = validate_task_group(data)
        if errors:
            raise ValidationError(errors)
        super().validate_create(user, **data)


def validate_task_group(data, uuid=None):
    return [
        *validate_not_empty_field(data.get("code"), "code"),
        *validate_bf_unique_code(data.get('code'), uuid),
    ]


def validate_bf_unique_code(code, uuid=None):
    instance = TaskGroup.objects.filter(code=code, is_deleted=False).first()
    if instance and instance.uuid != uuid:
        return [{"message": _("tasks_management.validation.task_group.code_exists" % {
            'code': code
        })}]
    return []


def validate_not_empty_field(string, field):
    if not string:
        return [{"message": _("tasks_management.validation.field_empty") % {
            'field': field
        }}]
    return []
