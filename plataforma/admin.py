from django.contrib import admin
from .models import (DiasVisita, 
                    Cidade, Imagem, 
                    Horario, Imovel, Visita)

# Deixar o ADMIN do django mais organizado
@admin.register(Imovel) # buscar da classe  models/imovel
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('rua', 'valor', 'quartos', 'tamanho', 'cidade', 'tipo')
    list_editable = ('valor', 'tipo')
    list_filter = ('cidade', 'tipo')


admin.site.register(DiasVisita)
admin.site.register(Cidade)
admin.site.register(Imagem)
admin.site.register(Horario)
admin.site.register(Visita)
#admin.site.register(Imovel) # remover o umovel daqui para a class acima funcionar

