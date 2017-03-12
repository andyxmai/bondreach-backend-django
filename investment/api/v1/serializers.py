from investment.models import InvestmentType
from rest_framework import serializers


class InvestmentTypeSerializer(serializers.ModelSerializer):

  id = serializers.UUIDField(required=False)
  
  class Meta:
    model = InvestmentType
    fields = ('id', 'name')