from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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


class Period(BaseModel):
    start = models.DateTimeField(
        _('Period start date'),
        default=timezone.now,
    )
    end = models.DateTimeField(
        _('Period end date'),
        default=timezone.now,
    )


    def __str__(self):
        period_name = f'{self.start.date()}-{self.end.date()}'
        return period_name

    class Meta:
        get_latest_by = "start"
