import uuid
from customer.models import Customer, Team
from django.contrib.postgres.fields import JSONField
from django.db import models
from utils.dates import utcnow


class TeamEventCategory(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  
  created_at = models.DateTimeField(default=utcnow)
  description = models.TextField(default='', blank=True)
  name = models.CharField(max_length=200, unique=True)

  class Meta:
    ordering = ('name',)
    verbose_name_plural = "Team event categories"

  def __str__(self):
    return self.name  


class TeamEvent(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  
  created_at = models.DateTimeField(default=utcnow)
  created_by = models.ForeignKey(Customer, related_name='events', on_delete=models.CASCADE)

  team = models.ForeignKey(Team, blank=True, related_name='events', on_delete=models.CASCADE)
  category = models.ForeignKey('TeamEventCategory', related_name='events', on_delete=models.CASCADE)

  metadata = JSONField(default={}, blank=True)