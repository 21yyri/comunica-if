from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

import requests

from ..models import Usuario

SUAP_API = "https://suap.ifrn.edu.br/api"

class Login(APIView):
    def post(self, request):
        username, password = request.data.values()

        if not (username and password):
            return Response({
                "msg": "Usuário ou senha vazios"
            }, status=400)
        
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "Token": token.key
            }, status=200)
        
        try:
            token = self.get_suap_token(username, password)
        except requests.HTTPError:
            return Response({
                "msg": "Usuário inválido"
            }, status=401)
        
        try:
            user = self._create_user(username, password, token)
        except:
            return Response({
                "msg": "Campus não autorizado."
            }, status=403)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "Token": token.key
        }, status=201)


    def get_suap_token(self, username, password):
        response = requests.post(f"{SUAP_API}/token/pair", json={
            "username": username,
            "password": password,
        })
        response.raise_for_status()
        
        return response.json()["access"]


    def _create_user(self, username, password, token):
        response = requests.get(f"{SUAP_API}/rh/eu/", headers={
            "authorization": f"Bearer {token}"
        })

        user_data = response.json()
        if user_data["campus"] != "CM":
            raise Exception("Campus não autorizado.")

        return Usuario.objects.create_user(
            username=username,
            password=password,
            first_name=user_data["nome_social"] or user_data["primeiro_nome"],
            last_name=user_data["ultimo_nome"],
            email=user_data["email"],
            is_servidor=user_data["tipo_usuario"] == "Servidor",
        )
