from core.models import InteractiveUser
from tasks_management.models import Task
from tasks_management.models import TaskGroup

task_group_add_payload = {
    "code": "example",
    "completion_policy": TaskGroup.TaskGroupCompletionPolicy.ANY,
}

task_payload = {
    'source': 'test_source',
    'entity': InteractiveUser.objects.first(),
    'status': Task.Status.RECEIVED,
    'executor_action_event': 'test_executor_action',
    'business_status': dict(),
    'business_event': 'test_business_action',
    'data': dict()
}
