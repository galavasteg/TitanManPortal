from django.db import models
from django.utils import timezone


class HistoryModel(models.Model):
    modified_datetime = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.modified_datetime = timezone.now()
        return super().save(*args, **kwargs)

    @staticmethod
    def get_fields():
        return ('modified_datetime',)

    class Meta:
        abstract = True
