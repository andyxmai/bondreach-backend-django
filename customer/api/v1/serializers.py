from account.api.v1.serializers import UserSerializer
from customer.models import Customer, Team
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
  
  id = serializers.UUIDField(required=False)

  class Meta:
    model = Team
    fields = ('id', 'name')


class CustomerSerializer(serializers.ModelSerializer):

  id = serializers.UUIDField(required=False)
  user = UserSerializer(read_only=True)
  team = TeamSerializer(required=False)

  class Meta:
    model = Customer
    fields = ('id', 'user', 'team')
