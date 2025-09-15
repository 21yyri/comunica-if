from django.db import models
from .usuario import Usuario
from datetime import datetime
from PIL import Image

class Postagem(models.Model):
    class Meta:
        verbose_name_plural: str = 'Postagens'
    
    autor: Usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    body: str = models.CharField(max_length = 324)

    imagem: Image = models.ImageField(blank = True, upload_to = 'postagens/')

    data: datetime = models.DateTimeField(default = datetime.now())

    def __str__(self) -> str:
        return f'[{self.data}] {self.autor}: {self.body}'
