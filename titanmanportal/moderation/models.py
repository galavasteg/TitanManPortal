from django.db import models
from django.db.models import PROTECT, CASCADE
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

import utils.models
from periods.models import Period
from users.models import User


class Moderation(utils.models.HistoryModel):

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

    def __str__(self):
        moderates = self.users.count()
        # TODO: [moderates / all active users on period]
        s = f'{self.period}: {self.moderator}' \
            f' {_("проверяет цели у")} {moderates}'
        return s


class ModerationToUser(models.Model):

    moderation = models.ForeignKey(
        Moderation,
        on_delete=models.CASCADE,
        related_name='moderation2member',
    )
    user = models.ForeignKey(
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

    def __str__(self):
        s = f'{self.user}'
        return s


class Goal(utils.models.HistoryModel):

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
    description = models.CharField(
        _('Описание цели'),
        max_length=500,
        null=False, blank=False,
        default=_('Какая цель?')
    )
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

    class Meta:
        get_latest_by = "period"

    def __str__(self):
        s = f'{self.description[:20]}'
        return s


class Proof(models.Model):

    class TYPES:
        IMG = 'image'
        LINK = 'link'
        TEXT = 'text'
    TYPE_CHOICES = (
        (TYPES.IMG, _('фото/скрин')),
        (TYPES.LINK, _('ссылка')),
        (TYPES.TEXT, _('текст')),
    )
    type = models.CharField(
        _('Тип пруфа'),
        max_length=20,
        choices=TYPE_CHOICES,
    )

    proof_image = models.ImageField(
        _('Фото/скрин'),
        blank=True, null=True,
    )
    proof_link = models.URLField(
        _('Ссылка'),
        max_length=128,
        blank=True, null=True,
    )
    proof_text = models.TextField(
        _('Ссылка'),
        max_length=1000,
        blank=True, null=True,
    )

    goal = models.ForeignKey(
        Goal,
        on_delete=CASCADE
    )
    description = models.CharField(
        _('Описание пруфа'),
        max_length=500,
        null=False, blank=False,
        default=_('Какой пруф?')
    )

    class STATE:
        NEW = 'new'
        ACCEPTED = 'accepted'
        CONFIRMED = 'confirmed'
        EXPIRED = 'expired'
        REJECTED = 'rejected'
    state = FSMField(
        _('Статус пруфа'),
        default=STATE.NEW,
        protected=True,
    )

    @transition(
        state, source=STATE.NEW, target=STATE.ACCEPTED,
    )
    def to_accepted(self):
        """Proof accepted by moderator"""

    @transition(
        state, source=STATE.ACCEPTED, target=STATE.CONFIRMED,
    )
    def to_confirmed(self):
        """Proof confirmed by moderator"""

    @transition(
        state, source=STATE.ACCEPTED, target=STATE.REJECTED,
    )
    def to_rejected(self):
        """Proof rejected by moderator"""

    @transition(
        state, source=STATE.ACCEPTED, target=STATE.EXPIRED,
    )
    def to_expired(self):
        """Period is done and proof not provided by member"""

    def __str__(self):
        s = f'{self.description[:20]}'
        return s
