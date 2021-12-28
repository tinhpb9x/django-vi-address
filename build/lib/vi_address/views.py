from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import City, District
from .serializers import (
    CitySerializer,
    CityDetailSerializer,
    DistrictDetailSerializer
)


class CityAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityDetailAPIView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer


class DistrictDetailAPIView(RetrieveAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer
