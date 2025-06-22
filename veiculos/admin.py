from django.contrib import admin
from .models import Veiculo, RegistroMovimento


class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'placa',
                    'odometro', 'ano_fabricacao', 'chassi')


class RegistroMovimentoAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'veiculo',
                    'data_saida', 'odometro_saida',
                    'data_chegada', 'odometro_chegada')

admin.site.register(Veiculo, VeiculoAdmin)
admin.site.register(RegistroMovimento, RegistroMovimentoAdmin)
