from django.contrib import admin
from .models import Usuario, Postagem

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass


@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    pass
