from event.api.v1.serializers import TeamEventSerializer
from event.models import TeamEvent
from rest_framework import viewsets


class TeamEventViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """

  serializer_class = TeamEventSerializer

  def get_queryset(self):
    try:
      user = self.request.user
      creator = user.customer_profile
      team = creator.team

      queryset = TeamEvent.objects.filter(team=team).order_by('-created_at')    
    except:  # TODO (Andy): break down the exceptions and log them
      queryset = TeamEvent.objects.none()

    return queryset