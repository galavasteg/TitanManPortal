from django.core.mail import send_mail

from periods import services
from rating.models import Rating
from users.models import User


def get_name_initials(user: User):
    initials = (f'{str(user.first_name)[0]}.'
                # f'{str(user.middle_name)[0]}.'
                f' {user.last_name}')
    return initials


def email_user(user, subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [user.email], **kwargs)


def add_rating_to_created_user_callback(
        sender: type(User), instance: User,
        created: bool, *args, **kwargs):
    user = instance
    if created:
        period = services.get_current_period()

        rating = Rating(period=period, user=user)
        user.rating.set([rating], bulk=False)
