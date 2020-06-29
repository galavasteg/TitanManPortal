from django.db import models
from django.db.models import PROTECT
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from _utils.models import HistoryModel
from periods.models import Period
from users.models import User


class Moderation(HistoryModel):

    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        related_name='moderators',
    )
    moderator = models.ForeignKey(
        User,
        on_delete=PROTECT,
        related_name='moderates',
    )
    users = models.ManyToManyField(
        User,
        through='ModerationToUser',
        # related_name='moderated_by',
    )


class ModerationToUser(models.Model):

    moderation = models.ForeignKey(
        Moderation,
        on_delete=models.CASCADE,
        related_name='moderation2member',
    )
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='moderated_by',
        # parent_link=True,
    )

    class STATE:
        TO_ACCEPT = 'to_accept'
        ACCEPTED = 'accepted'
        READY_TO_CHECK = 'ready'
        GOALS_FAILED = 'failed'
        SUCCESS = 'success'

    state = FSMField(
        _('Статус модерации'),
        default=STATE.TO_ACCEPT,
        editable=True,
    )

    @transition(
            field=state,
            source=STATE.TO_ACCEPT,
            target=STATE.ACCEPTED,
            conditions=(
                # TODO all goals accepted
            ),
        )
    def accept(self):
        self.state = self.STATE.ACCEPTED


class Goal(HistoryModel):
    user = models.ForeignKey(
        User,
        on_delete=PROTECT,
        # related_name='goals',
    )
    period = models.ForeignKey(
        Period,
        on_delete=PROTECT,
        # related_name='goals',
    )

    class STATE:
        NEW = 'new'
        ACCEPTED = 'accepted'
        ON_MODERATION = 'on_moderation'
        SUCCESS = 'success'
        EXPIRED = 'expired'  # TODO: expired is failed
        FAILED = 'failed'

    state = FSMField(
        _('Статус цели'),
        default=STATE.NEW,
        protected=True,
    )
