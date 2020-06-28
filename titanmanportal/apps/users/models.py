from pathlib import Path

from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
        BaseUserManager,
        AbstractBaseUser,
        PermissionsMixin,
    )
from phonenumber_field.modelfields import PhoneNumberField

from _utils.models import HistoryModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, phone_number: str,
                     is_staff: bool, is_superuser: bool, **extra_fields):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        extra_fields = {**dict(is_active=True), **extra_fields}

        user = self.model(email=email, phone_number=phone_number,
                          is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, phone_number: str,
                    **extra_fields):
        return self._create_user(email, password, phone_number,
                                 False, False, **extra_fields)

    def create_staffuser(self, email, password, phone_number: str,
                         **extra_fields):
        return self._create_user(email, password, phone_number,
                                 True, False, **extra_fields)

    def create_superuser(self, email, password, phone_number: str,
                         **extra_fields):
        extra_fields = dict(**extra_fields, is_active=True)
        return self._create_user(email, password, phone_number,
                                 True, True, **extra_fields)


class User(AbstractBaseUser, HistoryModel, PermissionsMixin):

    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user is already registered with this e-mail address."),
        },)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)

    phone_verified = models.BooleanField(
        _('phone verification status'),
        default=False,
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=False,
        help_text=_('Designates whether the user can log in'),
    )

    def path_profile_photo(self, filename: str) -> str:
        p = Path('profile_photos') / str(self.pk) / filename
        return str(p)
    photo = models.ImageField('Photo',
            # dimensions from 600x600px to 8000x8000px, max 6m
            upload_to=path_profile_photo, null=True, blank=True)

    not_verified_email = models.EmailField(
            _('new email address'),
            unique=True, blank=True, null=True,
            error_messages={
                'unique': _("A user is already registered with "
                            "this e-mail address."),
            },)
    reset_pwd_security_code = models.CharField(
            _('reset pwd code'), max_length=8, null=True, blank=False)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ('phone_number', )

    def __str__(self):
        return self.email


# TODO to apps -> ready()
from .services import ProfileService
post_save.connect(ProfileService.post_user_save, sender=User)
