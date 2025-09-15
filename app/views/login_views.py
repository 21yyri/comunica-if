from typing import Union
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..models import Usuario
import requests

suapi_url = 'https://suap.ifrn.edu.br/api'


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Verifica a existência de usuário
        usuario: Usuario = authenticate(request, username = username, password = password)
        if usuario:
            token, _ = Token.objects.get_or_create(user = usuario)
            return Response({
                "Token": token.key
            }, status = 200)


        # Adquirindo token para requisições ao SUAPI
        try:
            token: str = self._get_suap_token(username, password)
        except Exception as e:
            return Response({
                "msg": "usuário inválido."
            }, status = 404)


        # Dando fetch em dados do usuário
        try:
            user_data: dict = self._get_user_data({
                "Authorization": f"Bearer {token}"
            })
        except requests.exceptions.RequestException:
            return Response({
                "msg": "Não foi possível dar fetch nos dados."
            }, status = 400)


        # Validando o campus
        if not user_data.get("campus") == "CM":
            return Response({
                "msg": "Campus não autorizado."
            }, status = 403)


        # Coleta dados e cria usuário no banco de dados
        nome: str = user_data.get("nome_social") or user_data.get("nome_registro")
        partes_nome: list[str] = nome.split()

        new_usuario = Usuario.objects.create(
            username = username,
            first_name = partes_nome[0],
            last_name = partes_nome[-1],
            nome_completo = nome,
            is_staff = user_data.get("tipo_usuario") == "Servidor",
            email = user_data.get("email")
        )

        new_usuario.set_password(password)
        new_usuario.save()

        token, _ = Token.objects.get_or_create(user = new_usuario)

        return Response({
            "Token": token.key
        }, status = 201)
    

    def _get_suap_token(self, username, password) -> str | None:
        """Usa as credenciais para adquirir o token de requisições do suap."""
        try:
            response = requests.post(
                f"{suapi_url}/token/pair", json = {
                    "username": username,
                    "password": password
                }
            )
            response.raise_for_status()

            return response.json().get("access")
        except requests.exceptions.RequestException:
            raise Exception("Usuário inválido.")


    def _get_user_data(self, authorization: dict) -> dict:
        """Usa o token para adquirir informações do usuário."""
        try:
            response = requests.get(
                f'{suapi_url}/rh/eu/', headers=authorization
            )
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException:
            raise Exception("Requisição inválida.")
