import graphene
from graphene_django import DjangoObjectType

from core import ExtendedConnection, prefix_filterset
from core.gql_queries import UserGQLType
from tasks_management.models import TaskGroup, TaskExecutor, Task


class TaskGQLType(DjangoObjectType):
    uuid = graphene.String(source='uuid')

    class Meta:
        model = Task
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "entity_type": ["exact"],
            "entity_id": ["exact"],

            "source": ["iexact", "istartswith", "icontains"],
            "status": ["iexact", "istartswith", "icontains"],
            "executor_action_event": ["iexact", "istartswith", "icontains"],
            "business_event": ["iexact", "istartswith", "icontains"],

            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"],
            "version": ["exact"],
        }
        connection_class = ExtendedConnection


class TaskGroupGQLType(DjangoObjectType):
    uuid = graphene.String(source='uuid')
    user = graphene.List(UserGQLType)

    class Meta:
        model = TaskGroup
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "code": ["exact", "iexact", "startswith", "istartswith", "contains", "icontains"],
            "completion_policy": ["exact", "iexact"],

            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"],
            "version": ["exact"],
        }
        connection_class = ExtendedConnection

    def resolve_user(self, info):
        task_group_id = self.id
        return TaskExecutor.objects.filter(task_group_id=task_group_id)


class TaskExecutorGQLType(DjangoObjectType):
    uuid = graphene.String(source='uuid')

    class Meta:
        model = TaskExecutor
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            **prefix_filterset("user__", UserGQLType._meta.filter_fields),
            **prefix_filterset("task_group__", TaskGroupGQLType._meta.filter_fields),
            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"],
            "version": ["exact"],
        }
        connection_class = ExtendedConnection
