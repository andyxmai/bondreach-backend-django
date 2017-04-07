import uuid
from contact.utils import get_upcoming_follow_up
from customer.models import Customer
from django.db import models
from investment.models import InvestmentType
from region.models import Region
from utils.dates import utcnow


class Contact(models.Model):
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(default=utcnow)

  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100, blank=True)
  email = models.EmailField(blank=True)
  phone = models.CharField(max_length=100, blank=True)
  company = models.CharField(max_length=200, blank=True)

  region_preferences = models.ManyToManyField(Region, related_name='interested_contacts', blank=True)
  investment_type_preferences = models.ManyToManyField(InvestmentType, related_name='interested_contacts', blank=True)

  minimum_investment_size = models.IntegerField(blank=True)
  maximum_investment_size = models.IntegerField(blank=True)

  # IRR return preference: from 0 to 100%
  minimum_irr_return = models.PositiveSmallIntegerField(blank=True, default=0)
  maximum_irr_return = models.PositiveSmallIntegerField(blank=True, default=100)

  EQUITY = 'EQUITY'
  DEBT = 'DEBT'
  INVESTMENT_SIZE_CHOICES = (
    (EQUITY, 'equity'),
    (DEBT, 'debt'),
  )
  investment_type = models.CharField(max_length=100, blank=True, choices=INVESTMENT_SIZE_CHOICES)

  notes = models.TextField(null=True, blank=True)

  creator = models.ForeignKey(Customer, related_name='contacts', null=True, blank=True, on_delete=models.CASCADE)

  def __str__(self):
    return self.first_name + " " + self.last_name

  def get_upcoming_follow_up(self):
    follow_up = FollowUp.objects.filter(contact=self).first()
    if follow_up:
      upcoming_follow_up = get_upcoming_follow_up(follow_up.begin_date, follow_up.frequency)
      if upcoming_follow_up is not None:
        return upcoming_follow_up

    return ''


class FollowUp(models.Model):

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(default=utcnow)
  is_active = models.BooleanField(default=True)

  begin_date = models.DateField()
  frequency = models.CharField(max_length=100)

  contact = models.ForeignKey('Contact', related_name='follow_ups', null=True, on_delete=models.CASCADE)

  def __str__(self):
    return "{} {} ({}, {})".format(self.contact.first_name, self.contact.last_name, self.begin_date, self.frequency)


class Correspondence(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(default=utcnow)

  correspondence_type = models.TextField(blank=True)
  date = models.DateTimeField(null=True, blank=True)
  item_id = models.TextField(blank=True)
  contact = models.ForeignKey('Contact', related_name='correspondences', null=True, on_delete=models.CASCADE)

  def __str__(self):
    return "{} {} ({})".format(self.contact.first_name, self.contact.last_name, self.correspondence_type)
