from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

import moderation.models
import rating.models
import users.models
import periods.models

MAIN_GROUP = "Administrator"

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
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):

        # add all permision to main group
        admin_group, created = Group.objects.get_or_create(name=MAIN_GROUP)
        permissions_list = Permission.objects.all()
        admin_group.permissions.set(permissions_list)
        self.stdout.write("Adding all permisions to group " + MAIN_GROUP)
        # add all permision in group

        permissions_list = Permission.objects.all()
        admin_group.permissions.set(permissions_list)

        # Loop groups
        for group_name in GROUPS_PERMISSIONS:

            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:

                # Loop permissions in group/model
                for perm_index, perm_name in enumerate(
                    GROUPS_PERMISSIONS[group_name][model_cls]
                ):

                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.filter(
                            content_type__app_label=model_cls._meta.app_label
                        ).get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write(
                            "Adding " + codename + " to group " + group.__str__()
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
