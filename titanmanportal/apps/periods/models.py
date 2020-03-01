from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (
        BaseUserManager,
        AbstractBaseUser,
        PermissionsMixin,
    )
from phonenumber_field.modelfields import PhoneNumberField


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


class Period(BaseModel, PermissionsMixin):
    start = models.DateTimeField(
        _('Period start date'),
        editable=False,
        null=True, blank=True,
    )
    end = models.DateTimeField(
        _('Period end date'),
        editable=False,
        null=True, blank=True,
    )

    get_latest_by = "start"

    def __str__(self):
        period_name = f'{self.start.date}-{self.end.date}'
        return period_name

