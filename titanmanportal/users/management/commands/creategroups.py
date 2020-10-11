from typing import Dict, Sequence

import django.db.models
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db import transaction

import moderation.models
import rating.models
import users.models
import periods.models

ModelToPermissions = Dict[django.db.models.Model, Sequence[str]]


ADMIN_GROUP = "Administrator"

GROUPS_PERMISSIONS = {
    "Участник": {
        users.models.User: ["view"],
        rating.models.Rating: ["view"],
        rating.models.Beginner: ["view"],
        periods.models.Period: ["view"],
        moderation.models.ModerationToUser: ["view"],
        moderation.models.Moderation: ["change", "view"],
        moderation.models.Goal: ["add", "change", "delete", "view"],
    },
    "Модератор": {
        users.models.User: ["view"],
        rating.models.Rating: ["view"],
        rating.models.Beginner: ["view"],
        periods.models.Period: ["view"],
        moderation.models.ModerationToUser: ["view"],
        moderation.models.Moderation: ["change", "view"],
        moderation.models.Goal: ["add", "change", "delete", "view"],
    },
}


def set_all_permissions_to_admin(admin_group: str) -> None:
    admin_group, _ = Group.objects.get_or_create(name=admin_group)
    permissions_list = Permission.objects.all()
    admin_group.permissions.set(permissions_list)
    permissions_list = Permission.objects.all()
    admin_group.permissions.set(permissions_list)


def set_premissions_to_group(group: Group,
                             model_actions_map: ModelToPermissions
                             ) -> None:
    for model_cls, actions in model_actions_map.items():
        for action in actions:
            # Generate permission name as Django would generate it
            codename = f'{action}_{model_cls._meta.model_name}'

            # Find permission object and add to group
            try:
                model_permissions = Permission.objects.filter(
                    content_type__app_label=model_cls._meta.app_label)
                perm = model_permissions.get(codename=codename)
                group.permissions.add(perm)
                print("Added", codename, "to group", str(group))
            except Permission.DoesNotExist:
                print(codename + " not found")


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        # add all permission to main group
        # TODO: logging
        # TODO: check that groups and permissions set already
        print("Adding all permissions for", ADMIN_GROUP)
        with transaction.atomic():
            set_all_permissions_to_admin(ADMIN_GROUP)

            for group_name, model_actions_map in GROUPS_PERMISSIONS.items():
                group, _ = Group.objects.get_or_create(name=group_name)

                set_premissions_to_group(group, model_actions_map)
