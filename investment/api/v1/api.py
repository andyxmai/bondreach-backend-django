from investment.api.v1.serializers import InvestmentTypeSerializer
from investment.models import InvestmentType
from rest_framework import viewsets


class InvestmentTypeViewSet(viewsets.ReadOnlyModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """

  queryset = InvestmentType.objects.all()
  serializer_class = InvestmentTypeSerializer