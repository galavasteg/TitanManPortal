from django.db import models
from django.db.models import PROTECT
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from periods.models import Period


User = get_user_model()


class BaseModel(models.Model):
    modified_datetime = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.modified_datetime = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    @staticmethod
    def get_fields():
        return 'modified_datetime',

    class Meta:
        abstract = True


class Moderation(BaseModel):

    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        related_name='moderation',
    )
    moderator = models.ForeignKey(
        User,
        on_delete=PROTECT,
        related_name='moderates',
    )
    members = models.ManyToManyField(
        User,
        related_name='moderated_by',
    )
