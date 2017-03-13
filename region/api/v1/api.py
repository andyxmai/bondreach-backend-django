from region.models import Region
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from region.api.v1.serializers import RegionSerializer
from region.permissions import IsReadOnly

class RegionViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  permission_classes = (IsAuthenticated, IsReadOnly)

  queryset = Region.objects.all()
  serializer_class = RegionSerializer