from django.db import models
from django.utils.translation import gettext_lazy as _


class Caixa(models.Model):
    empresa = models.ForeignKey("core.Empresa", on_delete=models.CASCADE)
    banco = models.CharField(max_length=100)
    agencia = models.IntegerField()
    conta = models.IntegerField()
    saldo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.empresa} - {self.banco}"


class CategoriaFinanceira(models.Model):
    TIPO_CATEGORIA = [
        ('RE', 'Receita'),
        ('DE', 'Despesa'),
    ]

    nome = models.CharField(max_length=100)
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TIPO_CATEGORIA)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Categoria Financeira')
        verbose_name_plural = _('Categorias Financeiras')

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"



class Contrato(models.Model):
    STATUS_CHOICES = [
        ('PE', 'Pendente'),
        ('CO', 'Confirmado'),
        ('AN', 'Cancelado'),
        ('RE', 'Realizado'),
        ('PA', 'Pago'),
    ]
    evento = models.ForeignKey("eventos.Evento", on_delete=models.SET_NULL, null=True, blank=True)
    responsavel = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Responsável pelo Contrato'))
    arquivo = models.FileField(upload_to="arquivos/", blank=True, null=True, verbose_name=_('Arquivo'))
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PE')
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.evento} - {self.get_status_display()}"


class LancamentoFinanceiro(models.Model):
    STATUS_CHOICES = [
        ('PE', 'Pendente'),
        ('PA', 'Pago'),
        ('CA', 'Cancelado'),
    ]

    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(CategoriaFinanceira, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_vencimento = models.DateField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PE')
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Lançamento Financeiro')
        verbose_name_plural = _('Lançamentos Financeiros')
        ordering = ['-data_vencimento']

    def __str__(self):
        return f"{self.categoria} - R${self.valor} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.id:
            if self.categoria.tipo == 'RE':
                if self.contrato:
                    self.contrato.evento.valor_total += self.valor
            elif self.categoria.tipo == 'DE':
                if self.contrato:
                    self.contrato.evento.valor_custo += self.valor
            self.contrato.evento.save()
            if self.status == 'PA' and self.categoria.tipo == 'DE':
                self.categoria.caixa.saldo -= self.valor
            elif self.status == 'PA' and self.categoria.tipo == 'RE':
                self.categoria.caixa.saldo += self.valor
        else:
            old_instance = LancamentoFinanceiro.objects.get(id=self.id)
            if old_instance.valor != self.valor:
                if self.categoria.tipo == 'RE':
                    if self.contrato:
                        self.contrato.evento.valor_total -= old_instance.valor
                        self.contrato.evento.valor_total += self.valor
                elif self.categoria.tipo == 'DE':
                    if self.contrato:
                        self.contrato.evento.valor_custo -= old_instance.valor
                        self.contrato.evento.valor_custo += self.valor
                if self.status == 'PA' and self.categoria.tipo == 'DE':
                    self.categoria.caixa.saldo += old_instance.valor
                    self.categoria.caixa.saldo -= self.valor
                elif self.status == 'PA' and self.categoria.tipo == 'RE':
                    self.categoria.caixa.saldo -= old_instance.valor
                    self.categoria.caixa.saldo += self.valor
            else:
                if self.status == 'PA' and self.categoria.tipo == 'DE':
                    self.categoria.caixa.saldo -= self.valor
                elif self.status == 'PA' and self.categoria.tipo == 'RE':
                    self.categoria.caixa.saldo += self.valor
        self.categoria.caixa.save()
        self.contrato.evento.save()
        super().save(*args, **kwargs)


