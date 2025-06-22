from django.contrib import admin
from .models import (Cliente, Funcao,
                     Funcionario, Empresa,
                     Documento, DadosBancariosFunc,
                     EnderecoFunc, EnderecoCliente,
                     ContatoCliente, InfoFiscal)


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj')


class ClienteAdmin(admin.ModelAdmin):
    exclude = ('data_cadastro',)
    list_display = ('nome', 'tipo', 'cpf_cnpj',
                    'email', 'telefone', 'esta_ativo')

    def esta_ativo(self, obj):
        if obj.ativo:
            return 'Sim'
        else:
            return 'Não'


class FuncionarioAdmin(admin.ModelAdmin):
    exclude = ('usuario',)

    list_display = ('nome', 'tipo', 'cpf',
                    'funcao', 'telefone', 'email',
                    'data_admissao', 'tem_foto', 'esta_ativo')

    def tem_foto(self, obj):
        if obj.foto:
            return 'Sim'
        else:
            return 'Não'

    def esta_ativo(self, obj):
        if obj.ativo:
            return 'Sim'
        else:
            return 'Não'


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'nome', 'tem_arquivo', 'vencimento')

    def tem_arquivo(self, obj):
        if obj.arquivo:
            return 'Sim'
        else:
            return 'Não'


class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_hora', 'esta_ativo')

    def esta_ativo(self, obj):
        if obj.ativo:
            return 'Sim'
        else:
            return 'Não'


class DadosBancariosFuncAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'nome_banco', 'nr_bco',
                    'agencia', 'conta', 'pix')


class EnderecoFuncAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'logadouro', 'numero',
                    'complemento', 'bairro', 'cidade', 'cep')


class EnderecoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'logadouro', 'numero',
                    'complemento', 'bairro', 'cidade', 'cep')


class ContatoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'nome', 'email', 'cargo', 'telefone')


class InfoFiscalAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'inscricao_estadual', 'inscricao_municipal')


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Funcao, FuncaoAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(DadosBancariosFunc, DadosBancariosFuncAdmin)
admin.site.register(EnderecoFunc, EnderecoFuncAdmin)
admin.site.register(EnderecoCliente, EnderecoClienteAdmin)
admin.site.register(ContatoCliente, ContatoClienteAdmin)
admin.site.register(InfoFiscal, InfoFiscalAdmin)
