# from rest_framework import generics
from rest_framework import viewsets

from api.paginators import RatePagination
from api.serializers import RateSerializer
from currency.models import Rate


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = RatePagination

# class RatesView(generics.ListCreateAPIView):
#     queryset = Rate.objects.all()
#     serializer_class = RateSerializer
#
#
# class RateDetailsView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rate.objects.all()
#     serializer_class = RateSerializer
