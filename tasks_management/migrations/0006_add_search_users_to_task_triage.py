from django.db import migrations
from core.utils import insert_role_right_for_system, remove_role_right_for_system

users_search_right = 121701
task_triage = 2097152


def add_rights(apps, schema_editor):
    insert_role_right_for_system(task_triage, users_search_right, apps )


def remove_rights(apps, schema_editor):
    remove_role_right_for_system(task_triage, users_search_right, apps )



class Migration(migrations.Migration):
    dependencies = [
        ('tasks_management', '0005_add_task_perms_to_admin')
    ]

    operations = [
        migrations.RunPython(add_rights, remove_rights),
    ]
