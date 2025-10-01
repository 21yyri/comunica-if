from django.db import models
from .usuario import Usuario
from datetime import datetime
from PIL import Image

class Noticia(models.Model):
    class Meta:
        verbose_name_plural: str = 'Notícias'
    
    autor: Usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    setor: str = models.CharField(max_length = 15, null = True)

    titulo: str = models.CharField(max_length = 150)
    body: str = models.TextField()

    imagem: Image = models.ImageField(blank = True, null = True, upload_to = 'noticias/', max_length = 200)
    imagem_url: str = models.URLField(null = True)
    
    link: str = models.CharField(max_length = 220, default = None)
    data: datetime = models.DateTimeField(auto_now = True)

    disponivel: bool = models.BooleanField(default = True)
