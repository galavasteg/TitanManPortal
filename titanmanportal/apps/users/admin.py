from django.contrib import admin
from django.contrib.admin import sites
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...
    # fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": (
    #                 "email",
    #                 "phone_number",
    #             ),
    #         },
    #     ),
    #     (
    #         _("Personal info"),
    #         {
    #             "fields": (
    #                 "first_name",
    #                 "last_name",
    #                 "photo",
    #             ),
    #         },
    #     ),
    #     (
    #         _("Permissions"),
    #         {
    #             "fields": (
    #                 "is_active",
    #                 "groups",
    #             ),
    #         },
    #     ),
    #     (
    #         _("Important dates"),
    #         {
    #             "fields": (
    #                 "last_login",
    #                 "date_joined",
    #             ),
    #         },
    #     ),
    # )
    #
    # list_display = ("email", "first_name", "last_name", )

