from django import forms
from django.contrib import admin

from periods.services import PeriodService
from .models import Moderation
from .services import ModerationService


class Users2ModerateInlineAdmin(admin.TabularInline):
    model = Moderation.users.through
    fields = ('user',)
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':

            kwargs["queryset"] = ModerationService.get_queryset()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ModerationAdminForm(forms.ModelForm):

    class Meta:
        fields = ('period', 'moderator')
        model = Moderation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # request = args[0]
        # self.initial['moderator'] = request.user
        self.initial['period'] = PeriodService.get_current_period()


@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    form = ModerationAdminForm

    # readonly_fields = form._meta.fields
    inlines = (Users2ModerateInlineAdmin,)
