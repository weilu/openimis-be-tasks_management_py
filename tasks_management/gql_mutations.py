import graphene as graphene
from django.contrib.auth.models import AnonymousUser
from pydantic.error_wrappers import ValidationError

from core.gql.gql_mutations.base_mutation import BaseHistoryModelCreateMutationMixin, BaseMutation
from core.schema import OpenIMISMutation
from tasks_management.apps import TasksManagementConfig
from tasks_management.models import TaskGroup


class CreateTaskGroup(OpenIMISMutation.Input):
    class TaskGroupCompletionPolicyEnum(graphene.Enum):
        ALL = TaskGroup.TaskGroupCompletionPolicy.ALL
        ANY = TaskGroup.TaskGroupCompletionPolicy.ANY
        N = TaskGroup.TaskGroupCompletionPolicy.N

    code = graphene.String(required=True, max_length=255)
    completion_policy = graphene.Field(TaskGroupCompletionPolicyEnum, required=True)
    user_ids = graphene.List(graphene.UUID)

    def resolve_completion_policy(self, info):
        return self.completion_policy


class CreateTaskGroupMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "CreateTaskGroupMutation"
    _mutation_module = "tasks_management"
    _model = TaskGroup

    @classmethod
    def _validate_mutation(cls, user, **data):
        if type(user) is AnonymousUser or not user.has_perms(
                TasksManagementConfig.gql_task_group_create_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def _mutate(cls, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = TaskGroupService(user)
        res = service.create(data)
        if not res['success']:
            return res
        return None

    class Input(CreateTaskGroup):
        pass
