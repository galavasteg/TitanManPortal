from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


class Profile:

    def __init__(self, user: User):
        self.user = user

    def get_name_initials(self):
        user = self.user
        initials = (f'{str(user.first_name)[0]}.'
                    f'{str(user.middle_name)[0]}.'
                    f' {user.last_name}')
        return initials

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], **kwargs)

