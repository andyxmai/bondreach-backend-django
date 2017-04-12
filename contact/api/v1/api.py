import django_filters
from contact.models import Contact, FollowUp, Correspondence
from contact.utils import filter_contact_queryset
from contact.api.v1.serializers import ContactSerializer, FollowUpSerializer, CorrespondenceSerializer, ContactCompanySerialzier
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models import Min, Max
from rest_framework.filters import SearchFilter
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination


class ContactFilter(django_filters.rest_framework.FilterSet):
  class Meta:
    model = Contact
    fields = ['investment_type_preferences', 'region_preferences', 'email', 'company']


class ContactViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """

  serializer_class = ContactSerializer
  filter_backends = (django_filters.rest_framework.DjangoFilterBackend, SearchFilter,)
  filter_class = ContactFilter
  # Note (Andy): this is not going to be scalable. Will need ElasticSearch at some point
  search_fields = ('notes', '^first_name', '^last_name', 'company')

  def get_queryset(self):
    try:
      user = self.request.user
      creator = user.customer_profile
      team = creator.team
      investment_size = self.request.query_params.get('investment_size', None)
      target_return = self.request.query_params.get('target_return', None)

      queryset = filter_contact_queryset(team, creator, investment_size, target_return)
    except:  # TODO (Andy): break down the exceptions and log them
      queryset = Contact.objects.none()

    return queryset


"""
This extra endpoint is used because pagination needs to be turned off when downloading
data.
Note (Andy): need to fix the duplication
"""
class DownloadContactViewSet(viewsets.ReadOnlyModelViewSet):
  pagination_class = None

  serializer_class = ContactSerializer
  filter_backends = (django_filters.rest_framework.DjangoFilterBackend, SearchFilter,)
  filter_class = ContactFilter
  # Note (Andy): this is not going to be scalable. Will need ElasticSearch at some point
  search_fields = ('notes', '^first_name', '^last_name', 'company')

  def get_queryset(self):
    try:
      user = self.request.user
      creator = user.customer_profile
      team = creator.team
      investment_size = self.request.query_params.get('investment_size', None)
      target_return = self.request.query_params.get('target_return', None)
      
      queryset = filter_contact_queryset(team, creator, investment_size, target_return)
    except:  # TODO (Andy): break down the exceptions and log them
      queryset = Contact.objects.none()

    return queryset


class ContactCompanyViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = ContactCompanySerialzier
  filter_backends = (django_filters.rest_framework.DjangoFilterBackend, SearchFilter,)
  filter_class = ContactFilter
  # Note (Andy): this is not going to be scalable. Will need ElasticSearch at some point
  search_fields = ('notes', '^first_name', '^last_name', 'company')

  def get_queryset(self):
    try:
      user = self.request.user
      creator = user.customer_profile
      team = creator.team
      investment_size = self.request.query_params.get('investment_size', None)
      target_return = self.request.query_params.get('target_return', None)

      queryset = filter_contact_queryset(team, creator, investment_size, target_return)
    except:  # TODO: break down the exceptions and log them
      queryset = Contact.objects.none()

    return queryset.values('company').annotate(
            minimum_investment_size=Min('minimum_investment_size'), 
            maximum_investment_size=Max('maximum_investment_size'),
            minimum_irr_return=Min('minimum_irr_return'),
            maximum_irr_return=Min('maximum_irr_return'),
            first_names=ArrayAgg('first_name'),
            last_names=ArrayAgg('last_name'),
            emails=ArrayAgg('email'),
          )


class DownloadContactCompanyViewSet(viewsets.ReadOnlyModelViewSet):
  pagination_class = None

  serializer_class = ContactCompanySerialzier
  filter_backends = (django_filters.rest_framework.DjangoFilterBackend, SearchFilter,)
  filter_class = ContactFilter
  # Note (Andy): this is not going to be scalable. Will need ElasticSearch at some point
  search_fields = ('notes', '^first_name', '^last_name', 'company')

  def get_queryset(self):
    try:
      user = self.request.user
      creator = user.customer_profile
      team = creator.team
      investment_size = self.request.query_params.get('investment_size', None)
      target_return = self.request.query_params.get('target_return', None)

      queryset = filter_contact_queryset(team, creator, investment_size, target_return)
    except:  # TODO: break down the exceptions and log them
      queryset = Contact.objects.none()

    return queryset.values('company').annotate(
            minimum_investment_size=Min('minimum_investment_size'), 
            maximum_investment_size=Max('maximum_investment_size'),
            minimum_irr_return=Min('minimum_irr_return'),
            maximum_irr_return=Min('maximum_irr_return'),
            first_names=ArrayAgg('first_name'),
            last_names=ArrayAgg('last_name'),
            emails=ArrayAgg('email'),
          )


class FollowUpViewSet(viewsets.ModelViewSet):
  queryset = FollowUp.objects.all()
  serializer_class = FollowUpSerializer


class CorrespondenceViewSet(viewsets.ModelViewSet):
  queryset = Correspondence.objects.all().order_by('-date')
  serializer_class = CorrespondenceSerializer