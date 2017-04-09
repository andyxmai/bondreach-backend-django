from feed.models import NewsFeed
from rest_framework import serializers


class NewsFeedSerializer(serializers.ModelSerializer):

  id = serializers.UUIDField(required=False)
  
  class Meta:
    model = NewsFeed
    fields = ('id', 'company', 'name', 'url', 'date_published')