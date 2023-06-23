from django.db import models
from django.utils.translation import gettext as _

from core.models import HistoryModel, User


class TaskGroup(HistoryModel):
    class TaskGroupCompletionPolicy(models.TextChoices):
        ALL = 'ALL', _('ALL')
        ANY = 'ANY', _('ANY')
        N = 'N', _('N')

    code = models.CharField(max_length=255, null=False, blank=False)
    completion_policy = models.CharField(
        max_length=50, choices=TaskGroupCompletionPolicy.choices, null=False, blank=False
    )


class TaskExecutor(HistoryModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    task_group = models.ForeignKey(TaskGroup, on_delete=models.DO_NOTHING, null=False)


class Task(HistoryModel):
    task_group = models.ForeignKey(TaskGroup, on_delete=models.DO_NOTHING)
