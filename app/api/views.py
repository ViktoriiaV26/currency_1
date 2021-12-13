from rest_framework import generics
from rest_framework import serializers

from currency.models import Rate


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = (
            'id',
            'sale',
            'buy',
        )


class RatesView(generics.ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer