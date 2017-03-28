from account.api.v1.serializers import UserSerializer
from customer.models import Customer, Company
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
  id = serializers.UUIDField(required=False)

  class Meta:
    model = Company
    fields = ('id', 'name')


class CustomerSerializer(serializers.ModelSerializer):

  id = serializers.UUIDField(required=False)
  user = UserSerializer(read_only=True)
  company = CompanySerializer(read_only=True)

  class Meta:
    model = Customer
    fields = ('id', 'user', 'company')
