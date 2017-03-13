from investment.api.v1.serializers import InvestmentTypeSerializer
from investment.models import InvestmentType
from investment.permissions import IsReadOnly
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class InvestmentTypeViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  permission_classes = (IsAuthenticated, IsReadOnly)

  queryset = InvestmentType.objects.all()
  serializer_class = InvestmentTypeSerializer