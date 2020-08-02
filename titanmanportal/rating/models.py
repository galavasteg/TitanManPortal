from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

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


class Rating(BaseModel):

    class LEAGUE:
        BEGINNER = "beginner"
        CORE = "core"
        MASTER = "master"

    league = FSMField(
        default=LEAGUE.BEGINNER,
        editable=False,
    )

    # TODO:
    # goal: fee, status

    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        related_name='rating',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='rating',
    )

    def rating_delta(self):
        return self.beginner_rating.delta
    rating_delta.short_description = _('Изменение рейтинга')

    def current_rating(self):
        return self.beginner_rating.current_rating
    current_rating.short_description = _('Текущий рейтинг')

    @transition(
            field=league,
            source=LEAGUE.BEGINNER,
            target=LEAGUE.CORE,
            conditions=(
                # TODO
            ),
        )
    def beginner2core(self):
        self.end_time = timezone.now()

    class Meta:
        get_latest_by = "period"


class Beginner(BaseModel):

    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name='beginner_rating',
    )
    delta = models.IntegerField(
        _('Изменение рейтинга'),
        default=0,
    )
    value = models.IntegerField(
        _('Значение'),
        null=True,
        editable=False,
    )
