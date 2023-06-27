from tasks_management.models import TaskGroup

task_group_add_payload = {
    "code": "example",
    "completion_policy": TaskGroup.TaskGroupCompletionPolicy.ANY,
}
