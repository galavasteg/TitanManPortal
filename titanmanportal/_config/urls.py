"""titanmanportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.utils.translation import ugettext_lazy as _
# import allauth.socialaccount.providers.vk
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.forms import SignupForm
admin.site.site_header = _('TitanManClub Portal')
admin.site.index_title = _('Portal administration')
admin.site.site_title = _('TitanManClub Portal')
admin.site.login = login_required(admin.site.login)

urlpatterns = [
    path('', admin.site.urls),
    re_path(r'^accounts/', include('allauth.urls')),
]