from typing import Union, Iterable

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django_fsm import has_transition_perm

from users.models import User
from periods import services
from moderation.models import Moderation, Goal


def get_available_to_moderate_user_qs(moder: User,
        ) -> Union[QuerySet, Iterable[User]]:
    qs = User.objects.exclude(pk=moder.pk)
    return qs


def get_user_current_goal_qs(user: User) -> User.objects:
    period = services.get_current_period()
    qs = Goal.objects.filter(user=user, period=period)
    return qs


def set_goal_on_moderation(goal, initiator: User) -> None:
    assert has_transition_perm(goal.to_moderation, initiator), (
            f"{_('Недостаточно прав')} {_('или')}"
            f" {_('выполнены не все условия отправки на модерацию')}")
    goal.to_moderation()
    goal.save()


# def add_member_to_moder(cls, moder: User,
#                         member: User,
#                         period: PeriodService.PERIOD_MODEL):
#     err_msg = ''
#     if moder is not member:
#         err_msg = _('Moderator cannot moderates himself')
#     # TODO: check league?
#
#     if err_msg:
#         raise AttributeError(err_msg)
#
#     members = moder.moderates.filter(period=period).all()
#     members.add(member)
#     moder.save()
