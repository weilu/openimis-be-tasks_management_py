from django.apps import AppConfig

DEFAULT_CONFIG = {
    "gql_task_group_search_perms": ["190001"],
    "gql_task_group_create_perms": ["190002"],
    "gql_task_group_update_perms": ["190003"],
    "gql_task_group_delete_perms": ["190004"],
}


class TasksManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks_management'

    gql_task_group_search_perms = None
    gql_task_group_create_perms = None
    gql_task_group_update_perms = None
    gql_task_group_delete_perms = None

    def ready(self):
        from core.models import ModuleConfiguration

        print("Hello automatic update")

        cfg = ModuleConfiguration.get_or_default(self.name, DEFAULT_CONFIG)
        self.__load_config(cfg)

    @classmethod
    def __load_config(cls, cfg):
        """
        Load all config fields that match current AppConfig class fields, all custom fields have to be loaded separately
        """
        for field in cfg:
            if hasattr(TasksManagementConfig, field):
                setattr(TasksManagementConfig, field, cfg[field])
