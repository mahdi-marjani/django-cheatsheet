from rest_framework.generics import (
    GenericAPIView
)
from .models import Car
from .serializers import CarSerializer
from rest_framework.response import Response

class Home(GenericAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        ser_data = self.get_serializer(instance).data
        return Response(ser_data)