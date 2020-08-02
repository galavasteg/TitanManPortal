from typing import Union, Iterable

from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

import periods.services
from .models import Moderation, Goal, Proof
from . import services


class Users2ModerateInlineAdmin(admin.TabularInline):
    model = Moderation.users.through
    readonly_fields = ('state',)
    fields = ('user', *readonly_fields)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':

            kwargs['queryset'] = services.get_available_to_moderate_user_qs(
                    request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ModerationAdminForm(forms.ModelForm):

    class Meta:
        fields = ('period', 'moderator')
        model = Moderation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # request = args[0]
        # self.initial['moderator'] = request.user
        self.initial['period'] = periods.services.get_current_period()


@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    form = ModerationAdminForm

    # readonly_fields = form._meta.fields
    inlines = (Users2ModerateInlineAdmin,)


class ProofsInlineAdmin(admin.StackedInline):
    model = Proof
    readonly_fields = ('state',)
    fieldsets = (
        (
            None, dict(fields=('description', *readonly_fields)),
        ),
        (
            None, dict(fields=(
                'type', 'proof_image', 'proof_link', 'proof_text',),
            ),
        ),
    )
    extra = 0


class GoalAdminForm(forms.ModelForm):

    class Meta:
        fields = ('period', 'user')
        model = Goal

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['period'] = periods.services.get_current_period()

    # def save(self, commit=True):


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    # form = GoalAdminForm

    readonly_fields = ('period', 'state',)
    fields = ('description', *readonly_fields)
    list_display = fields
    actions = ('on_moderation',)
    inlines = (ProofsInlineAdmin,)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            'proof_type/js/hide_other_proof_fields.js',
        )

    def get_queryset(self, request):
        user = request.user
        qs = services.get_user_current_goal_qs(user)
        return qs

    def save_form(self, request, form, change):
        goal = super().save_form(request, form, change)
        goal.user = request.user
        goal.period = periods.services.get_current_period()
        return goal

    def on_moderation(self, request, goals_qs: Union[QuerySet, Iterable[Goal]]):
        with transaction.atomic():
            try:
                for goal in goals_qs:
                    services.set_goal_on_moderation(goal, request.user)
            except AssertionError as e:
                self.message_user(request, str(e), level=messages.WARNING)
    on_moderation.short_description = _('Отправить на модерацию')

