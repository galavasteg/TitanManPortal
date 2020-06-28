from allauth.account.signals import user_signed_up
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    verbose_name = _("УЧАСТНИКИ КЛУБА")
    name = 'users'

    def ready(self):
        from .signals.handlers import (
            user_signed_up_callback,
        )

        user_signed_up.connect(user_signed_up_callback)
