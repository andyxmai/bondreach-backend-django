from event.models import TeamEvent
from rest_framework import serializers


class TeamEventSerializer(serializers.ModelSerializer):

  id = serializers.UUIDField(required=False)

  class Meta:
    model = TeamEvent
    fields = ('id', 'created_at', 'created_by', 'team', 'category', 'metadata')