from rest_framework.views import APIView
from ..models import Postagem, Noticia
from ..serializers import NoticiaSerializer, PostagemSerializer
from datetime import datetime, timedelta
from rest_framework.response import Response


class Carrossel(APIView):
    noticias = Noticia.objects.filter(
        data__gte = datetime.now() - timedelta(hours = 12),
        disponivel = True
    ).order_by('data')

    postagens = Postagem.objects.filter(
        data__gte = datetime.now() - timedelta(hours = 12), 
        disponivel = True
    ).order_by('data')


    def get(self, request):
        noticias_serial = NoticiaSerializer(self.noticias, many = True).data
        postagens_serial = PostagemSerializer(self.postagens, many = True).data

        if not postagens_serial:
            return Response(noticias_serial, status = 200)
        
        if not noticias_serial:
            return Response(postagens_serial, status = 200)

        i = 0
        conteudo = []
        while True:
            if not noticias_serial and not postagens_serial:
                break
            try:
                if i % 5 == 0:
                    conteudo.append(postagens_serial[-1])
                    postagens_serial.pop()
                else:
                    conteudo.append(noticias_serial[-1])
                    noticias_serial.pop()
            except IndexError:
                pass

            i += 1

        return Response(conteudo, status = 200)
