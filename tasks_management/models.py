from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from core.models import HistoryModel


class Task(HistoryModel):
    class Status(models.TextChoices):
        RECEIVED = 'RECEIVED', _('Received')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')

    source = models.CharField(max_length=255, null=False)
    entity_type = models.ForeignKey(ContentType, models.DO_NOTHING, null=True, unique=False)
    entity_id = models.CharField(max_length=255, null=True)
    entity = GenericForeignKey('entity_type', 'entity_id')
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.RECEIVED)
    executor_action_event = models.CharField(max_length=255, null=True)
    business_status = models.JSONField(default=dict)
    business_event = models.CharField(max_length=255, null=True)
