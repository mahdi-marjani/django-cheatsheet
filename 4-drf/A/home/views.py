from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class Home(APIView):
    permission_classes = [IsAdminUser,]

    def get(self, request):
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True)
        return Response({"data": ser_data.data})
