import graphene
from graphene_django import DjangoObjectType

from core import ExtendedConnection
from tasks_management.models import TaskGroup


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
