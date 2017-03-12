import uuid
from django.db import models
from utils.dates import utcnow


class Region(models.Model):
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(default=utcnow)

  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name