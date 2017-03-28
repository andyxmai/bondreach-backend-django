import uuid
from account.models import User
from django.db import models
from utils.dates import utcnow


class Customer(models.Model):

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(default=utcnow)

  user = models.OneToOneField(User, related_name='_customer_profile', on_delete=models.CASCADE)
  company = models.ForeignKey('Company', null=True, blank=True, related_name='employees', on_delete=models.CASCADE)

  def __str__(self):
    return self.user.email


class Company(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(default=utcnow)
  is_active = models.BooleanField(default=True)

  name = models.CharField(max_length=200, blank=True)
  allow_contact_sharing = models.BooleanField(default=False, blank=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'companies'