import copy

from django.test import TestCase

from core.test_helpers import create_test_interactive_user
from tasks_management.tests.data import task_payload
from tasks_management.services import TaskService
from tasks_management.models import Task


class TaskServiceTestCase(TestCase):
    user = None
    service = None

    @classmethod
    def setUpClass(cls):
        super(TaskServiceTestCase, cls).setUpClass()
        cls.user = create_test_interactive_user(username="test_admin")
        cls.service = TaskService(cls.user)

    def test_create_task(self):
        result = self.service.create(task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.RECEIVED)

    def test_update_task(self):
        result = self.service.create(task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        update_payload = copy.deepcopy(task_payload)
        update_payload['source'] = 'updated_source'
        update_payload['id'] = result['data']['uuid']
        result = self.service.update(update_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])

    def test_delete_task(self):
        result = self.service.create(task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        delete_payload = {'id': result['data']['uuid']}
        result = self.service.delete(delete_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])

    def test_execute_task(self):
        result = self.service.create(task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        execute_payload = {'id': result['data']['uuid']}
        result = self.service.execute_task(execute_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])

    def test_complete_task(self):
        result = self.service.create(task_payload)

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
        result = self.service.create(task_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        obj_id = result['data']['id']
        self.assertTrue(Task.objects.filter(id=obj_id).exists())

        complete_payload = {'id': result['data']['uuid'], 'failed': True}
        result = self.service.complete_task(complete_payload)

        self.assertTrue(result)
        self.assertTrue(result['success'])
        self.assertEqual(Task.objects.filter(id=obj_id).first().status, Task.Status.FAILED)
