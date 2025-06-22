from django.contrib import admin
from .models import (TipoEvento, Cardapio,
                     ItemCompraCardapio, Evento,
                     AlocacaoFuncionario, ConsumoEvento,
                     EnderecoEvento)


class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'esta_ativo')

    def esta_ativo(self, obj):
        if obj.ativo:
            return "Sim"
        else:
            return "Nao"


class CardapioAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em','atualizado_em',)
    list_display = ('nome', 'tipo_evento', 'preco_base',
                    'esta_ativo', 'data_criacao', 'ultima_atualizacao')

    def esta_ativo(self, obj):
        if obj.ativo:
            return "Sim"
        else:
            return "Nao"

    def data_criacao(self, obj):
        return obj.criado_em.strftime('%d/%m/%Y')

    def ultima_atualizacao(self, obj):
        return obj.atualizado_em.strftime('%d/%m/%Y')


class ItemCompraCardapioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cardapio', 'quantidade',
                    'unidade')


class EventoAdmin(admin.ModelAdmin):
    readonly_fields = ('valor_total','valor_custo',
                       'criado_em','atualizado_em',)
    list_display = ('nome_evento', 'tipo_evento', 'cliente',
                    'data_inicio', 'data_fim', 'numero_convidados',
                    'valor_total', 'valor_custo', 'lucro_estimado', 'status')


class AlocacaoFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'evento', 'valor')


class ConsumoEventoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'evento', 'quantidade',
                    'valor_unitario')


class EnderecoEventoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'logadouro', 'numero',
                    'complemento', 'bairro', 'cidade',
                    'cep')


admin.site.register(TipoEvento, TipoEventoAdmin)
admin.site.register(Cardapio, CardapioAdmin)
admin.site.register(ItemCompraCardapio, ItemCompraCardapioAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(AlocacaoFuncionario, AlocacaoFuncionarioAdmin)
admin.site.register(ConsumoEvento, ConsumoEventoAdmin)
admin.site.register(EnderecoEvento, EnderecoEventoAdmin)
