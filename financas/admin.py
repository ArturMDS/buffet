from django.contrib import admin
from .models import (Caixa, CategoriaFinanceira,
                     LancamentoFinanceiro, Contrato)


class CaixaAdmin(admin.ModelAdmin):
    list_display = ('banco', 'empresa', 'agencia',
                    'conta', 'saldo')


class CategoriaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'caixa', 'esta_ativo')

    def esta_ativo(self, obj):
        if obj.ativo:
            return "Sim"
        else:
            return "Não"

class ContratoAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em', 'atualizado_em')
    list_display = ('evento', 'tem_arquivo', 'status',
                    'data_criacao', 'ultima_atualizacao')

    def tem_arquivo(self, obj):
        if obj.arquivo:
            return 'Sim'
        else:
            return 'Não'

    def data_criacao(self, obj):
        return obj.criado_em.strftime('%d/%m/%Y')

    def ultima_atualizacao(self, obj):
        return obj.atualizado_em.strftime('%d/%m/%Y')


class LancamentoFinanceiroAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em', 'atualizado_em')
    list_display = ('valor', 'categoria', 'contrato',
                    'status', 'data_vencimento', 'data_pagamento')


admin.site.register(Caixa, CaixaAdmin)
admin.site.register(CategoriaFinanceira, CategoriaFinanceiraAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(LancamentoFinanceiro, LancamentoFinanceiroAdmin)

