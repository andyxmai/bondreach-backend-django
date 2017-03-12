from region.models import Region
from rest_framework import serializers


class RegionSerializer(serializers.ModelSerializer):

  id = serializers.UUIDField(required=False)
  
  class Meta:
    model = Region
    fields = ('id', 'name')