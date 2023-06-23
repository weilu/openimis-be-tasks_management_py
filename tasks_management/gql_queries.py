import graphene
from graphene_django import DjangoObjectType

from core import ExtendedConnection, prefix_filterset
from core.gql_queries import UserGQLType
from tasks_management.models import TaskGroup, TaskExecutor


class TaskGroupGQLType(DjangoObjectType):
    uuid = graphene.String(source='uuid')

    class Meta:
        model = TaskGroup
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "code": ["exact", "iexact", "startswith", "istartswith", "contains", "icontains"],
            "completion_policy": ["exact", "iexact"],
        }
        connection_class = ExtendedConnection


class TaskExecutorGQLType(DjangoObjectType):
    uuid = graphene.String(source='uuid')

    class Meta:
        model = TaskExecutor
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            **prefix_filterset("user__", UserGQLType._meta.filter_fields),
            **prefix_filterset("task_group__", TaskGroupGQLType._meta.filter_fields),
        }
        connection_class = ExtendedConnection
