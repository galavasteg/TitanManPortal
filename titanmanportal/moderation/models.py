from django.db import models
from django.db.models import PROTECT
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
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
    members = models.ManyToManyField(
        User,
        through='ModerationToMember',
        # related_name='moderated_by',
    )


class ModerationToMember(models.Model):

    moderation = models.ForeignKey(
        Moderation,
        on_delete=models.CASCADE,
        related_name='moderation2member',
    )
    member = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='moderated_by',
        # parent_link=True,
    )

    class STATE:
        TO_ACCEPT = "to_accept"
        ACCEPTED = "accepted"
        READY_TO_CHECK = "ready"
        GOALS_FAILED = "failed"
        SUCCESS = "success"

    state = FSMField(
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
