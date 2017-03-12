import django_filters
from contact.models import Contact, FollowUp
from rest_framework import permissions, viewsets
from contact.api.v1.serializers import ContactSerializer, FollowUpSerializer


class ContactFilter(django_filters.rest_framework.FilterSet):
  class Meta:
    model = Contact
    fields = ['investment_type_preferences', 'region_preferences', 'email']


class ContactViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """

  serializer_class = ContactSerializer
  filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
  filter_class = ContactFilter

  def get_queryset(self):
    try:
      user = self.request.user
      creator = user.customer_profile
      company = creator.company
      if company and company.allow_contact_sharing:
        queryset = Contact.objects.filter(creator__company_id=company.id)
      else:
        queryset = Contact.objects.filter(creator=creator)
      
      investment_size = self.request.query_params.get('investment_size', None)
      if investment_size is not None:
        queryset = queryset.filter(
          minimum_investment_size__lte=investment_size,
          maximum_investment_size__gte=investment_size
        )
    except:  # TODO (Andy): break down the exceptions and log them
      queryset = Contact.objects.none()

    return queryset


class FollowUpViewSet(viewsets.ModelViewSet):
  queryset = FollowUp.objects.all()
  serializer_class = FollowUpSerializer
