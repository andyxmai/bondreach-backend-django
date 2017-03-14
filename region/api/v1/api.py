from region.models import Region
from rest_framework import viewsets
from region.api.v1.serializers import RegionSerializer

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """

  queryset = Region.objects.all()
  serializer_class = RegionSerializer