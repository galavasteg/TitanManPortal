from typing import Iterable, Union

from django.db import models
from django.db.models import PROTECT, CASCADE, QuerySet
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition, GET_STATE

import utils.models
from periods.models import Period
from users.models import User


class Goal(utils.models.HistoryModel):

    class STATE:
        NEW = 'new'
        AGREED = 'accepted'
        MODERATION = 'on_moderation'
        ACHIEVED = 'achieved'
        EXPIRED = 'expired'  # TODO: expired is failed
        FAILED = 'failed'
    STATE_CHOICES = (
        (STATE.NEW, _('новая')),
        (STATE.AGREED, _('согласована')),
        (STATE.MODERATION, _('на проверке')),
        (STATE.ACHIEVED, _('выполнена')),
        (STATE.EXPIRED, _('просрочена')),
        (STATE.FAILED, _('не выполнена')),
    )
    state = FSMField(
        _('Статус цели'),
        default=STATE.NEW,
        choices=STATE_CHOICES,
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
        related_name='goals',
    )
    period = models.ForeignKey(
        Period,
        on_delete=PROTECT,
        related_name='goals',
    )

    def all_proofs_agreed(self):
        check = all(p.state == Proof.STATE.AGREED
                    for p in self.proofs.all())
        return check

    def all_proofs_provided(self):
        check = all(p.is_provided for p in self.proofs.all())
        return check

    def all_proofs_accepted(self):
        check = all(p.state == Proof.STATE.ACCEPTED
                    for p in self.proofs.all())
        return check

    def any_proof_expired(self):
        check = any(p.state == Proof.STATE.EXPIRED
                    for p in self.proofs.all())
        return check

    def any_proof_rejected(self):
        check = any(p.state == Proof.STATE.REJECTED
                    for p in self.proofs.all())
        return check

    @transition(
        state, source=STATE.NEW, target=STATE.AGREED,
        conditions=(all_proofs_agreed,),
    )
    def to_agreed(self):
        """Goal agreed with moderator"""

    @transition(
        state, source=STATE.AGREED, target=STATE.MODERATION,
        conditions=(all_proofs_provided, ),
    )
    def to_moderation(self):
        """Goal can be checked by moderator"""
        # TODO: email to moderator

    @transition(
        state, source=STATE.AGREED, target=STATE.EXPIRED,
        conditions=(any_proof_expired, ),
    )
    def to_expired(self):
        """Goal expired because of expiration its proof"""

    @transition(
        state, source=STATE.MODERATION, target=STATE.FAILED,
        conditions=(any_proof_rejected,),
    )
    def to_fail(self):
        """Goal failed because of rejected proof"""

    @transition(
        state, source=STATE.MODERATION, target=STATE.ACHIEVED,
        conditions=(all_proofs_accepted,),
    )
    def to_success(self):
        """Goal successfully achieved!"""

    class Meta:
        get_latest_by = "period"

    def __str__(self):
        s = f'{self.description[:20]}'
        return s


class Proof(models.Model):

    class TYPE:
        IMG = 'image'
        LINK = 'link'
        TEXT = 'text'
    TYPE_CHOICES = (
        (TYPE.IMG, _('фото/скрин')),
        (TYPE.LINK, _('ссылка')),
        (TYPE.TEXT, _('текст')),
    )
    type = models.CharField(
        _('Тип пруфа'),
        max_length=20,
        choices=TYPE_CHOICES,
    )

    TYPE_FIELD_MAP = {
        TYPE.IMG: 'proof_image',
        TYPE.LINK: 'proof_link',
        TYPE.TEXT: 'proof_text',
    }
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
        _('Текст'),
        max_length=1000,
        blank=True, null=True,
    )

    @property
    def is_provided(self) -> bool:
        field_name = self.TYPE_FIELD_MAP[self.type]
        provided = bool(getattr(self, field_name))
        return provided

    goal = models.ForeignKey(
        Goal, on_delete=CASCADE,
        related_name='proofs'
    )
    description = models.CharField(
        _('Описание пруфа'),
        max_length=500,
        null=False, blank=False,
        default=_('Какой пруф?')
    )

    class STATE:
        NEW = 'new'
        AGREED = 'agreed'
        ACCEPTED = 'accepted'
        EXPIRED = 'expired'
        REJECTED = 'rejected'
    STATE_CHOICES = (
        (STATE.NEW, _('новый')),
        (STATE.AGREED, _('согласован')),
        (STATE.ACCEPTED, _('принят')),
        (STATE.EXPIRED, _('просрочен')),
        (STATE.REJECTED, _('отклонен')),
    )
    state = FSMField(
        _('Статус пруфа'),
        default=STATE.NEW,
        protected=True,
    )

    @transition(
        state, source=STATE.NEW, target=STATE.AGREED,
    )
    def to_agreed(self):
        """Proof agreed with moderator"""

    @transition(
        state, source=STATE.AGREED, target=STATE.ACCEPTED,
    )
    def to_accepted(self):
        """Provided proof accepted by moderator"""

    @transition(
        state, source=STATE.AGREED, target=STATE.REJECTED,
    )
    def to_rejected(self):
        """Provided proof rejected by moderator"""

    @transition(
        state, source=STATE.AGREED, target=STATE.EXPIRED,
        conditions=(not is_provided)
    )
    def to_expired(self):
        """Proof not provided by member and period is over"""

    def __str__(self):
        s = f'{self.description[:20]}'
        return s


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
        related_name='moderation2user',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='moderated_through',
    )

    class STATE:
        NEW = 'new'
        NO_GOALS = 'no_goals'
        GOALS_AGREED = 'goals_agreed'
        PERIOD_FAILED = 'period_failed'
        SUCCESS = 'success'
    STATE_CHOICES = (
        (STATE.NEW, _('новая модерация')),
        (STATE.GOALS_AGREED, _('цели согласованы')),
        (STATE.NO_GOALS, _('нет целей')),
        (STATE.PERIOD_FAILED, _('ПРОВАЛ')),
        (STATE.SUCCESS, _('УСПЕХ')),
    )
    state = FSMField(
        _('Статус модерации'),
        default=STATE.NO_GOALS,
        choices=STATE_CHOICES,
        protected=True,
    )

    def get_goals(self) -> Union[QuerySet, Iterable[Goal]]:
        goals = self.user.goals.all().filter(
                period=self.moderation.period)
        return goals

    def all_goals_agreed(self) -> bool:
        c = all(g.STATE == Goal.STATE.AGREED
                for g in self.get_goals())
        return c

    def all_goals_on_moderation(self) -> bool:
        c = all(g.STATE == Goal.STATE.MODERATION
                for g in self.get_goals())
        return c

    def all_goals_achieved(self) -> bool:
        c = all(g.STATE == Goal.STATE.ACHIEVED
                for g in self.get_goals())
        return c

    def any_goal_failed(self) -> bool:
        c = any(g.STATE == Goal.STATE.FAILED
                for g in self.get_goals())
        return c

    def _get_agreed_state(self) -> str:
        goals_count = self.get_goals().count()
        state = (self.STATE.GOALS_AGREED if goals_count > 0 else
                 self.STATE.NO_GOALS)
        return state

    @transition(
        field=state,
        source=STATE.NEW,
        target=GET_STATE(
                _get_agreed_state,
                states=(STATE.GOALS_AGREED, STATE.NO_GOALS)),
        conditions=(all_goals_agreed,),
    )
    def to_agreed(self):
        """User goals agreed or not set"""

    @transition(
        field=state,
        source=STATE.GOALS_AGREED,
        target=STATE.SUCCESS,
        conditions=(all_goals_achieved,),
    )
    def to_success(self):
        """User achieved all goals on this period!"""

    @transition(
        field=state,
        source=STATE.GOALS_AGREED,
        target=STATE.PERIOD_FAILED,
        conditions=(any_goal_failed,),
    )
    def to_failed(self):
        """User failed some goals on this period"""

    def __str__(self):
        s = f'{self.user}'
        return s
