from typing import Sequence

from django.contrib import admin
from django.contrib.admin import sites
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('first_name', 'last_name', 'group', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('is_active', 'is_staff', 'groups',
                       'last_login', 'date_joined')
    # filter_horizontal = ('user_permissions', )
    def group(self, user) -> str:
        groups = user.groups.all()
        if groups:
            group = ', '.join(g.name for g in groups)
            return group
        else:
            return 'admin'

    def has_change_permission(self, request, obj=None) -> bool:
        user = request.user
        has_perm = user.is_superuser or user == obj
        return has_perm

    def get_readonly_fields(self, request, obj=None) -> Sequence:
        if request.user.is_superuser:
            return ('last_login', 'date_joined',)
        return self.readonly_fields
