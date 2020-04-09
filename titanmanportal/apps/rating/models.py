from django.db import models
from django.db.models import PROTECT
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
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
    member = models.ForeignKey(
        User,
        on_delete=PROTECT,
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


class BeginnerRatingDetail(BaseModel):

    rating = models.ForeignKey(
        Rating,
        on_delete=PROTECT,
        related_name='beginner_rating',
    )
    delta = models.IntegerField(
        _('Rating delta'),
        default=0,
    )
    current_rating = models.IntegerField(
        _('Current rating'),
        null=True,
        editable=False,
    )


from .services import RatingService
post_save.connect(RatingService.post_rating_save, sender=Rating)
