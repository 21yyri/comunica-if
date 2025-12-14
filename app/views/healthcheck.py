from rest_framework.views import APIView
from rest_framework.response import Response


class Healthcheck(APIView):
    def get(self, request):
        return Response({
            "heatlh": "ok"
        }, status=200)
