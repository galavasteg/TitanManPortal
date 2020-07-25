from allauth.account.signals import user_signed_up
from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    verbose_name = _("УЧАСТНИКИ КЛУБА")
    name = 'users'

    def ready(self):
        from .signals.handlers import (
            user_signed_up_callback,
        )
        from . import services
        from .models import User

        post_save.connect(
            services.add_rating_to_created_user_callback,
            sender=User)
        user_signed_up.connect(
                user_signed_up_callback)
