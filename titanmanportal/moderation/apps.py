from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ModerationConfig(AppConfig):
    verbose_name = _('Модерация')
    name = 'moderation'
