from django.contrib import admin

from .models import Moderation


@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    ...
