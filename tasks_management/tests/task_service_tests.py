import copy
from unittest import skip

from django.test import TestCase

from tasks_management.apps import TasksManagementConfig
from tasks_management.tests.data import TaskDataMixin
from tasks_management.services import TaskService, TaskGroupService
from tasks_management.models import Task
from core.test_helpers import LogInHelper


class TaskServiceTestCase(TestCase, TaskDataMixin):
    user = None
    task_executor = None
    service = None
    taskgroup_all = None
    taskgroup_any = None
    taskgroup_n = None

    @classmethod
    def setUpClass(cls):
        super(TaskServiceTestCase, cls).setUpClass()
        cls.user = LogInHelper().get_or_create_user_api()
        cls.task_executor = LogInHelper().get_or_create_user_api(
                username='TaskExecutor')
        cls.init_data()
        cls.taskgroup_all_id = cls.__create_taskgroup(cls.task_group_add_payload_all)
        cls.taskgroup_n_id = cls.__create_taskgroup(cls.task_group_add_payload_n)
        cls.taskgroup_any_id = cls.__create_taskgroup(cls.task_group_add_payload_any)
        cls.service = TaskService(cls.user)

    def test_create_task(self):
        result = self.service.create(self.task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.RECEIVED)

    def test_update_task(self):
        result = self.service.create(self.task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        update_payload = copy.deepcopy(self.task_payload)
        update_payload['source'] = 'updated_source'
        update_payload['id'] = result['data']['uuid']
        result = self.service.update(update_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])

    def test_delete_task(self):
        result = self.service.create(self.task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        delete_payload = {'id': result['data']['uuid']}
        result = self.service.delete(delete_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])

    def test_complete_task(self):
        result = self.service.create(self.task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        complete_payload = {'id': result['data']['uuid']}
        result = self.service.complete_task(complete_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.COMPLETED)

    def test_fail_task(self):
        result = self.service.create(self.task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        complete_payload = {'id': result['data']['uuid'], 'failed': True}
        result = self.service.complete_task(complete_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.FAILED)

    @skip('To be redeveloped')
    def test_resolve_task_any(self):
        create_payload = {
            **self.task_payload_resolve_any,
            "task_group_id": self.taskgroup_any_id
        }
        result = self.service.create(create_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        resolve_payload = {"id": result["data"]["uuid"],
                           "business_status": {"Jan Kowalski": TasksManagementConfig.task_user_approved}}
        result = self.service.resolve_task(resolve_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.COMPLETED)

    @skip('To be redeveloped')
    def test_resolve_task_all(self):
        create_payload = {
            **self.task_payload_resolve_all,
            "task_group_id": self.taskgroup_any_id
        }
        result = self.service.create(create_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        resolve_payload = {"id": result["data"]["uuid"],
                           "business_status": {"Jan Kowalski": TasksManagementConfig.task_user_approved,
                                               "Adam Kowal": TasksManagementConfig.task_user_approved}}
        result = self.service.resolve_task(resolve_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.COMPLETED)

    @skip('To be redeveloped')
    def test_resolve_task_n(self):
        create_payload = {
            **self.task_payload_resolve_n,
            "task_group_id": self.taskgroup_any_id
        }
        result = self.service.create(create_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        resolve_payload = {"id": result["data"]["uuid"],
                           "business_status": {"Jan Kowalski": TasksManagementConfig.task_user_approved}}
        result = self.service.resolve_task(resolve_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.COMPLETED)

    @classmethod
    def __create_taskgroup(cls, payload):
        object_data = {
            **payload,
            "user_ids": [cls.user.id, cls.task_executor.id]
        }

        obj = TaskGroupService(cls.user).create(object_data)
        group_id = obj.get("data")["id"]

        return group_id
