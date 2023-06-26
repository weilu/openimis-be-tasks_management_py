import graphene
from graphene_django import DjangoObjectType

from core import ExtendedConnection
from .models import Task


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
