from django.utils import timezone
import pytz
from pytz import utc

def utcnow():
  """
  Returns current datetime in UTC (with tzinfo=utc)
  """

  return timezone.now().replace(tzinfo=utc)