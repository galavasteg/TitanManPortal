from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.http import HttpResponse

from .models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        """
        TODO: check email whitelist (create model)
         for invitation strategy.
        """
        open_for_signup = True
        return open_for_signup

    def populate_user(self, request, sociallogin, data):
        u = super().populate_user(request, sociallogin, data)
        u.photo = sociallogin.account.extra_data.get('photo', None)
        return u

    def pre_social_login(self, request, sociallogin: SocialLogin):
        soc_emails = (ea.email for ea in sociallogin.email_addresses)
        user = User.objects.filter(email__in=soc_emails).first()

        if user and user != sociallogin.user:
            sociallogin.connect(request, user)

            response = HttpResponse()
            raise ImmediateHttpResponse(response)
