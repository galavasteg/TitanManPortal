from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'league', 'period', 'member',
        # 'rating_delta', 'current_rating',
    )
