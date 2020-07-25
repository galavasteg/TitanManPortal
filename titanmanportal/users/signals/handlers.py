from django.contrib.auth.models import Group


def user_signed_up_callback(request, user, **kwargs):
    # TODO: verify email before is_active = True
    user.is_active = True
    user.is_staff = True

    members_group = Group.objects.get(name='Участник')
    members_group.user_set.add(user)

    user.save()
