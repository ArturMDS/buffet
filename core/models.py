from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nome_fantasia}"


class Documento(models.Model):
    nome = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to="documentos/", blank=True, null=True, verbose_name=_('Arquivo'))
    vencimento = models.DateField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}"


class Cliente(models.Model):
    TIPO_CLIENTE = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
        ('GO', 'Governo'),
        ('ON', 'ONG'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TIPO_CLIENTE)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Funcao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    valor_hora = models.DecimalField(max_digits=8, decimal_places=2)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Função')
        verbose_name_plural = _('Funções')

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    TIPO_FUNC = [
        ('PE', 'Permanente'),
        ('PS', 'Prestador de Serviço')
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TIPO_FUNC, default='PS')
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    funcao = models.ForeignKey(Funcao, on_delete=models.SET_NULL, null=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    data_admissao = models.DateField()
    foto = models.ImageField(upload_to='funcionarios/', blank=True, null=True, verbose_name=_('Foto'))
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Colaborador')
        verbose_name_plural = _('Colaboradores')

    def __str__(self):
        return self.nome


class DadosBancariosFunc(models.Model):
    nome_banco = models.CharField(max_length=100, verbose_name=_('Nome do Banco'))
    nr_bco = models.CharField(max_length=100 ,verbose_name=_('Número do Banco'), null=True, blank=True)
    agencia = models.IntegerField()
    conta = models.IntegerField()
    pix = models.CharField(max_length=100, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Dados Bancários do Colaborador')
        verbose_name_plural = _('Dados Bancarios dos Colaboradores')

    def __str__(self):
        return f"{self.funcionario} ({self.nome_banco})"


class EnderecoFunc(models.Model):
    logadouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=100, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Endereços do Colaborador')
        verbose_name_plural = _('Endereços dos Colaboradores')

    def __str__(self):
        return f"{self.funcionario}"


class EnderecoCliente(models.Model):
    logadouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=100, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Endereços do Cliente')
        verbose_name_plural = _('Endereços dos Clientes')

    def __str__(self):
        return f"{self.cliente}"

class ContatoCliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cargo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Contatos do Cliente')
        verbose_name_plural = _('Contatos dos Clientes')

    def __str__(self):
        return f"{self.cliente}"


class InfoFiscal(models.Model):
    inscricao_estadual = models.CharField(max_length=100)
    inscricao_municipal = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Informação Fiscal')
        verbose_name_plural = _('Informações Fiscais')

    def __str__(self):
        return f"{self.cliente}"

