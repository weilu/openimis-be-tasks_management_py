from django.db import migrations

from core.models import Role, RoleRight

task_rights = [190001, 190002, 190003, 190004, 191001, 191002, 191003, 191004]
imis_administrator_system = 64


def add_rights(apps, schema_editor):
    role = Role.objects.get(is_system=imis_administrator_system)
    for right_id in task_rights:
        if not RoleRight.objects.filter(validity_to__isnull=True, role=role, right_id=right_id).exists():
            _add_right_for_role(role, right_id)


def _add_right_for_role(role, right_id):
    RoleRight.objects.create(role=role, right_id=right_id, audit_user_id=1)


def remove_rights(apps, schema_editor):
    RoleRight.objects.filter(
        role__is_system=imis_administrator_system,
        right_id__in=task_rights,
        validity_to__isnull=True
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('tasks_management', '0004_auto_20230622_0735')
    ]

    operations = [
        migrations.RunPython(add_rights, remove_rights),
    ]
