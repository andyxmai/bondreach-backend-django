from investment.models import InvestmentType
from rest_framework import viewsets
from investment.api.v1.serializers import InvestmentTypeSerializer


class InvestmentTypeViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = InvestmentType.objects.all()
  serializer_class = InvestmentTypeSerializer