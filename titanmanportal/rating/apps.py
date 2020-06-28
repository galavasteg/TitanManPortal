from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class RatingConfig(AppConfig):
    verbose_name = _('РЕЙТИНГ')
    name = 'rating'

    def ready(self):
        from .services import RatingService
        from .models import Rating

        post_save.connect(
                RatingService.rating_save_callback,
                sender=Rating)
