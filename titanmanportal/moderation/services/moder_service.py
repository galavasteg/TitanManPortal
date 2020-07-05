from typing import Tuple
from django.utils.translation import ugettext_lazy as _

from users.models import User
from periods.services import PeriodService
from moderation.models import Moderation


class ModerationService:

    @classmethod
    def get_user_qs(cls, exclude_users: Tuple[User] = ()
                    ) -> User.objects:
        qs = User.objects.filter()
        return qs

    @classmethod
    # @classmethod
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
