from django.urls import path
from . import views

urlpatterns = [
    path('cities', views.CityAPIView.as_view()),
    path('city/<pk>', views.CityDetailAPIView.as_view()),
    path('district/<pk>', views.DistrictDetailAPIView.as_view()),
]