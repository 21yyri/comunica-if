from rest_framework.views import APIView
from ..models import Postagem, Noticia
from ..serializers import NoticiaSerializer, PostagemSerializer
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from datetime import timedelta
from core import settings

import redis
import pickle

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)

class Carrossel(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        carrossel = redis_client.get("carrossel")
        if carrossel != None:
            return Response(pickle.loads(carrossel), status=200)

        noticias, postagens = self._get_content()

        # Se não tiver um, retorna o outro
        if not postagens:
            return Response(noticias, status = 200)
        if not noticias:
            return Response(postagens, status = 200)

        conteudo = []
        for i in range(max(len(postagens), len(noticias))):
            if not noticias and not postagens:
                break

            try:
                if i % 5 == 0:
                    conteudo.append(postagens[-1])
                    postagens.pop()
                else:
                    conteudo.append(noticias[-1])
                    noticias.pop()

            except IndexError:
                pass
        
        redis_client.setex("carrossel", timedelta(minutes=30), pickle.dumps(conteudo),)
        return Response(conteudo, status = 200)
    

    def _get_content(self):
        noticias = Noticia.objects.filter(
            data__gte = datetime.now() - timedelta(hours = 12),
            disponivel = True
        ).order_by('?')
        noticias_serial = NoticiaSerializer(noticias, many=True)

        postagens = Postagem.objects.filter(
            data__gte = datetime.now() - timedelta(hours = 12), 
        ).order_by('data')
        postagens_serial = PostagemSerializer(postagens, many=True)

        return noticias_serial.data, postagens_serial.data
