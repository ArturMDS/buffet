from django.db import models
from django.utils.translation import gettext_lazy as _
from estoque.models import UNIDADE_CHOICES


class TipoEvento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Tipo de Evento')
        verbose_name_plural = _('Tipos de Eventos')

    def __str__(self):
        return self.nome


class Cardapio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.SET_NULL, null=True, blank=True)
    preco_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cardápio')
        verbose_name_plural = _('Cardápios')

    def __str__(self):
        return f"{self.nome} - R${self.preco_base}"


class ItemCompraCardapio(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=3, choices=UNIDADE_CHOICES, default='UN')
    cardapio = models.ForeignKey(Cardapio, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Item do Cardápio')
        verbose_name_plural = _('Itens do Cardápio')

    def __str__(self):
        return f"{self.nome} ({self.quantidade})"


class Evento(models.Model):
    STATUS_CHOICES = [
        ('PE', 'Pendente'),
        ('CO', 'Confirmado'),
        ('AN', 'Cancelado'),
        ('RE', 'Realizado'),
        ('PA', 'Pago'),
    ]

    cliente = models.ForeignKey("core.Cliente", on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.SET_NULL, null=True)
    cardapio = models.ForeignKey(Cardapio, on_delete=models.SET_NULL, null=True)
    nome_evento = models.CharField(max_length=100)
    data_inicio = models.DateTimeField(verbose_name=_('Data de Inicio'), null=True, blank=True)
    data_fim = models.DateTimeField(verbose_name=_('Data de Fim'), null=True, blank=True)
    numero_convidados = models.PositiveIntegerField(verbose_name=_('Quantidade'))
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    valor_custo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PE')
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Evento')
        verbose_name_plural = _('Eventos')
        ordering = ['-data_inicio']

    def __str__(self):
        return f"{self.nome_evento}"

    @property
    def lucro_estimado(self):
        if self.valor_custo:
            return self.valor_total - self.valor_custo
        return None


class AlocacaoFuncionario(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='alocacoes')
    funcionario = models.ForeignKey("core.Funcionario", on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_pagamento = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    pago = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Alocação de Funcionário')
        verbose_name_plural = _('Alocações de Funcionários')

    def __str__(self):
        return f"{self.funcionario} - {self.evento}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.evento.valor_custo += self.valor
        else:
            old_instance = AlocacaoFuncionario.objects.get(id=self.evento.id)
            if old_instance.valor != self.valor:
                self.evento.valor_custo -= old_instance.valor
                self.evento.valor_custo += self.valor
        self.evento.save()
        super().save(*args, **kwargs)


class ConsumoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='consumos')
    produto = models.ForeignKey("estoque.Produto", on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Consumo do Evento - Estoque')
        verbose_name_plural = _('Consumos dos Eventos - Estoque')

    def __str__(self):
        return f"{self.produto} - {self.quantidade}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.evento.valor_custo += self.produto.preco_custo
            self.produto.quantidade_atual -= self.quantidade
        else:
            old_instance = ConsumoEvento.objects.get(id=self.id)
            if old_instance.valor_unitario != self.valor_unitario or old_instance.quantidade != self.quantidade:
                self.evento.valor_custo -= old_instance.produto.preco_custo
                self.produto.quantidade_atual += old_instance.quantidade
                self.evento.valor_custo += self.produto.preco_custo
                self.produto.quantidade_atual -= self.quantidade
        self.evento.save()
        self.produto.save()
        super().save(*args, **kwargs)


class EnderecoEvento(models.Model):
    logadouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=100, null=True, blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Endereços do Evento')
        verbose_name_plural = _('Endereços dos Eventos')

    def __str__(self):
        return f"{self.evento}"

