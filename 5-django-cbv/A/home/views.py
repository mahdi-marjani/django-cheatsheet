from rest_framework.generics import (
    ListAPIView, DestroyAPIView
)
from .models import Car
from .serializers import CarSerializer


class Home(ListAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

class CarDelete(DestroyAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    lookup_field = 'name'
    lookup_url_kwarg = 'car_name'