# openIMIS Backend tasks_management reference module
This repository holds the files of the openIMIS Backend Task Managemet reference module.
It is dedicated to be deployed as a module of [openimis-be_py](https://github.com/openimis/openimis-be_py).

## ORM mapping:
* task_management_task, task_management_historicaltask > Task
* task_management_taskgroup, task_management_historicaltaskgroup > TaskGroup
* task_management_taskexecutor, task_management_historicaltaskexecutor > TaskExecutor

## GraphQl Queries
* task, taskGroup, taskExecutor

## Services
- Task
  - create
  - update
  - delete
  - execute_task
  - complete_task
  - resolve_task
- TaskGroup
  - create
  - update
  - delete
- TaskExecutor
  - create
  - update
  - delete

## Configuration options (can be changed via core.ModuleConfiguration)
* gql_task_group_search_perms: 190001
* gql_task_group_create_perms: 190002
* gql_task_group_update_perms: 190003
* gql_task_group_delete_perms: 190004
* gql_task_search_perms: 191001
* gql_task_create_perms: 191002
* gql_task_update_perms: 191003
* gql_task_delete_perms: 191004


## openIMIS Modules Dependencies
- core

## Creating execution action handlers and business event handlers
When user action specified by the task is being passed to backend, the task service sends ``task_service.resolve_task`` signal. 
The approach for handler is to bind to ``after`` signal and check the specific ``executor_action_event`` of the task.
The same approach is used for business event handlers, being required to bind on ``task_service.complete_task``.

```Python
# in signals.py in any module
def bind_service_signals():
    bind_service_signal(
        'task_service.resolve_task',
        handler_hook,
        bind_type=ServiceSignalBindType.AFTER
    )

def handler_hook(**kwargs):
    pass
```
