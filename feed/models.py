import uuid
from django.db import models
from utils.dates import utcnow


class NewsFeed(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(default=utcnow)

  company = models.CharField(max_length=200)
  name = models.TextField()
  url = models.TextField()
  date_published = models.DateTimeField()

  def __str__(self):
    return "({}) {}".format(self.company, self.name)