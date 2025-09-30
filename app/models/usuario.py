from django.db import models
from django.contrib.auth.models import User

class Usuario(User):
    nome_completo: str = models.CharField(max_length = 150, default = '')
    class Meta:
        verbose_name: str = 'Usuário'


    def is_authorized(self):
        return self.is_staff
    

    def __str__(self) -> str:
        return self.username
