from contact.models import Contact
from feed.api.v1.serializers import NewsFeedSerializer
from feed.models import NewsFeed
from rest_framework import viewsets


class NewsFeedViewSet(viewsets.ReadOnlyModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """

  serializer_class = NewsFeedSerializer

  def get_queryset(self):
    try:
      user = self.request.user
      creator = user.customer_profile
      team = creator.team
      
      if team:
        contacts = Contact.objects.filter(creator__team_id=team.id)
      else:
        contacts = Contact.objects.filter(creator=creator)

      queryset = NewsFeed.objects.filter(company__in=contacts.values_list('company', flat=True)).order_by('-date_published')
    except:  # TODO (Andy): break down the exceptions and log them
      queryset = NewsFeed.objects.none()

    return queryset