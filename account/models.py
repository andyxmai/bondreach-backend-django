from __future__ import unicode_literals

import uuid
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from utils.dates import utcnow


class UserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
    """
    Creates and saves a User with the given email and password.
    """
    if not email:
        raise ValueError('The given email must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    user = self._create_user(email, password, **extra_fields)
    user.is_staff = True
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
  """
  Abstract User with the same behaviour as Django's default User but
  without a username field. Uses email as the USERNAME_FIELD for
  authentication.

  The following attributes are inherited from the superclasses:
          * password
          * last_login
          * is_superuser
  """
  email = models.EmailField(_('email address'), unique=True)
  first_name = models.CharField(_('first name'), max_length=255, default="", blank=True)
  last_name = models.CharField(_('last name'), max_length=255, default="", blank=True)
  date_joined = models.DateTimeField(_('date joined'), default=utcnow)
  is_active = models.BooleanField(_('active'), default=True)
  is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')

  def get_full_name(self):
    '''
    Returns the first_name plus the last_name, with a space in between.
    '''
    full_name = '%s %s' % (self.first_name, self.last_name)
    return full_name.strip()

  def get_short_name(self):
    '''
    Returns the short name for the user.
    '''
    return self.first_name

  def email_user(self, subject, message, from_email=None, **kwargs):
    '''
    Sends an email to this User.
    '''
    send_mail(subject, message, from_email, [self.email], **kwargs)

   # --------
  # Consumer
  # --------
  def get_customer_profile(self):
    from customer.models import Customer
    try:
      customer = Customer.objects.get(user_id=self.id)
      return customer
    except Customer.DoesNotExist:
      return None

  @property
  def customer_profile(self):
    return self.get_customer_profile()


class OutlookUser(models.Model):
  """
    Links Outlook user to Bondreach user
  """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  unique_identifier = models.TextField()  # unique id that Outlook gives during auth

  def __str__(self):
    return "Outlook user: " + self.unique_identifier
