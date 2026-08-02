from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import City
from .serializers import (
    CitySerializer,
    CityDetailSerializer,
)


class CityAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityDetailAPIView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer
