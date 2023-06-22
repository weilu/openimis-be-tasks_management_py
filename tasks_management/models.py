from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core import models as core_models


class Task(core_models.HistoryModel):
    class TaskStatus(models.TextChoices):
        RECEIVED = "RECEIVED",  _("RECEIVED")
        ACCEPTED = "ACCEPTED",  _("ACCEPTED")
        COMPLETED = "COMPLETED",  _("COMPLETED")
        FAILED = "FAILED",  _("FAILED")

    source = models.CharField(max_length=50, null=False) # benefit plan mutation
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True)
    object_id = models.PositiveIntegerField(null=True)
    entity = GenericForeignKey('content_type', 'object_id') # create null # update model
    status = models.CharField(
        max_length=100, choices=TaskStatus.choices, default=TaskStatus.RECEIVED, null=False
    )
    complete_action = models.CharField(max_length=200, null=False) # string z register signal
    business_status = models.JSONField(null=True)
    business_event = models.CharField(max_length=200, null=True)
    data = models.JSONField(null=True)
