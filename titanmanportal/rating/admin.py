from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'league', 'period', 'user',
        # 'rating_delta', 'current_rating',
    )
