from django import forms
from django.contrib import admin

from periods.services import PeriodService
from users.models import User
from .models import Moderation, ModerationToUser, Goal, Proof
from .services import ModerationService


class Users2ModerateInlineAdmin(admin.TabularInline):
    model = Moderation.users.through
    fields = ('user',)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':

            kwargs['queryset'] = ModerationService.get_user_qs()

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


class ProofsInlineAdmin(admin.TabularInline):
    model = Proof
    fields = ('description', 'state', 'type')
    readonly_fields = ('state',)
    extra = 0


class GoalAdminForm(forms.ModelForm):

    class Meta:
        fields = ('period', 'user')
        model = Goal

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['period'] = PeriodService.get_current_period()
        # self.initial['user'] = PeriodService.get_current_period()

    # def save(self, commit=True):


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    # form = GoalAdminForm

    readonly_fields = ('period', 'state',)
    fields = (
        *readonly_fields, 'description',
    )
    list_display = fields

    inlines = (ProofsInlineAdmin,)

    def get_queryset(self, request):
        user = request.user
        qs = ModerationService.get_user_current_goal_qs(user)
        return qs

    def save_form(self, request, form, change):
        goal = super().save_form(request, form, change)
        goal.user = request.user
        goal.period = PeriodService.get_current_period()
        return goal

