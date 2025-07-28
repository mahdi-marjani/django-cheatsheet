from rest_framework.response import Response
from rest_framework.views import APIView


class Home(APIView):
    def get(self, request):
        message = request.query_params['msg']
        return Response({"message": message})

    def post(self, request):
        message = request.data['msg']
        return Response({"message": message})