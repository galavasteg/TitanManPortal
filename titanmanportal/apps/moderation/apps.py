from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ModerationConfig(AppConfig):
    verbose_name = _('МОДЕРАЦИЯ')
    name = 'moderation'
