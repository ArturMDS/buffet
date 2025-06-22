from django.contrib import admin
from .models import (Categoria,
                     Fornecedor,
                     LocalEstoque,
                     Produto,
                     MovimentacaoEstoque,
                     Inventario,
                     ItemInventario,
                     EnderecoFornecedor,
                     EnderecoLocalEstoque)


class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em','atualizado_em',)
    list_display = ('nome', 'tipo',
                    'data_criacao', 'ultima_atualizacao')

    def data_criacao(self, obj):
        return obj.criado_em.strftime('%d/%m/%Y')

    def ultima_atualizacao(self, obj):
        return obj.atualizado_em.strftime('%d/%m/%Y')



class FornecedorAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em','atualizado_em',)
    list_display = ('nome', 'tipo', 'cpf_cnpj', 'email',
                    'telefone', 'esta_ativo',
                    'data_criacao', 'ultima_atualizacao')

    def esta_ativo(self, obj):
        if obj.ativo:
            return 'Sim'
        else:
            return 'Não'

    def data_criacao(self, obj):
        return obj.criado_em.strftime('%d/%m/%Y')

    def ultima_atualizacao(self, obj):
        return obj.atualizado_em.strftime('%d/%m/%Y')


class LocalEstoqueAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em','atualizado_em',)
    list_display = ('nome', 'responsavel', 'esta_ativo',
                    'data_criacao', 'ultima_atualizacao')

    def esta_ativo(self, obj):
        if obj.ativo:
            return 'Sim'
        else:
            return 'Não'

    def data_criacao(self, obj):
        return obj.criado_em.strftime('%d/%m/%Y')

    def ultima_atualizacao(self, obj):
        return obj.atualizado_em.strftime('%d/%m/%Y')


class ProdutoAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em','atualizado_em',)
    list_display = ('nome', 'marca', 'categoria', 'fornecedor',
                    'quantidade_atual', 'unidade_medida', 'localizacao',
                    'preco_custo', 'localizacao', 'data_validade', 'status')


class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    exclude = ('usuario',)
    readonly_fields = ('data_movimentacao','data_atualizacao',)
    list_display = ('produto', 'tipo', 'quantidade',
                    'local_origem', 'local_destino',
                    'data_movimentacao', 'data_atualizacao')


class InventarioAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_em', 'atualizado_em',)
    list_display = ('responsavel', 'local', 'data_inicio', 'data_fim',
                    'status', 'data_criacao', 'ultima_atualizacao')

    def data_criacao(self, obj):
        return obj.criado_em.strftime('%d/%m/%Y')

    def ultima_atualizacao(self, obj):
        return obj.atualizado_em.strftime('%d/%m/%Y')


class ItemInvetarioAdmin(admin.ModelAdmin):
    list_display = ('produto', 'inventario', 'quantidade_sistema', 'quantidade_fisica',
                    'conferido', 'data_conferencia', 'usuario_conferencia')


class EnderecoFornecedorAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'logadouro', 'numero',
                    'complemento', 'bairro', 'cidade', 'cep')


class EnderecoLocalEstoqueAdmin(admin.ModelAdmin):
    list_display = ('estoque', 'logadouro', 'numero',
                    'complemento', 'bairro', 'cidade', 'cep')


admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(LocalEstoque, LocalEstoqueAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(MovimentacaoEstoque, MovimentacaoEstoqueAdmin)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(ItemInventario, ItemInvetarioAdmin)
admin.site.register(EnderecoFornecedor, EnderecoFornecedorAdmin)
admin.site.register(EnderecoLocalEstoque, EnderecoLocalEstoqueAdmin)


