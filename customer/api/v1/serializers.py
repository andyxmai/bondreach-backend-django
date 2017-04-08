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

  def update(self, instance, validated_data):
    print(validated_data)
    team_data = validated_data.pop('team', None)

    for key, val in validated_data.items():
      setattr(instance, key, val)

    if team_data is not None:  # only go through updating if the argument was passed
      team = Team.objects.get(id=team_data['id'])
      instance.team = team

    instance.save()

    return instance
