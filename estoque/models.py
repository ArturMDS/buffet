from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


UNIDADE_CHOICES = [
        ('UN', 'Unidade'),
        ('PC', 'Peça'),
        ('KG', 'Quilograma'),
        ('GR', 'Grama'),
        ('LT', 'Litro'),
        ('MT', 'Metro'),
        ('M2', 'Metro Quadrado'),
        ('M3', 'Metro Cúbico'),
        ('CX', 'Caixa'),
        ('DZ', 'Dúzia'),
        ('SC', 'Saco'),
        ('FD', 'Fardo'),
        ('RL', 'Rolo'),
        ('PCT', 'Pacote'),
        ('TON', 'Tonelada'),
    ]


class Categoria(models.Model):
    TIPO_CATEGORIA = [
        ('AL', 'Alimento'),  # Carnes, frios, grãos, etc.
        ('BE', 'Bebida'),  # Refrigerantes, sucos, água, álcool
        ('LP', 'Limpeza'),  # Produtos de higiene e limpeza
        ('MA', 'Material'),  # Descartáveis, embalagens
        ('EQ', 'Equipamento'),  # Som, iluminação, cozinha
        ('VE', 'Veículo'),  # Transporte de equipamentos
        ('MB', 'Mobiliário'),  # Mesas, cadeiras, bancadas
        ('DE', 'Decoração'),  # Toalhas, arranjos, centros de mesa
        ('UT', 'Utensílios'),  # Talheres, pratos, copos
        ('UN', 'Uniforme'),  # Roupas de funcionários
        ('SE', 'Segurança'),  # Extintores, kit primeiros socorros
        ('EN', 'Energia'),  # Geradores, extensões
        ('FL', 'Floral'),  # Flores naturais ou artificiais
        ('TE', 'Têxtil'),  # Cortinas, capas de cadeira
        ('OU', 'Outros'),  # Itens não categorizados
    ]

    nome = models.CharField(max_length=100, verbose_name=_('Nome'))
    tipo = models.CharField(max_length=2, choices=TIPO_CATEGORIA, verbose_name=_('Tipo'))
    descricao = models.TextField(blank=True, null=True, verbose_name=_('Descrição'))
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Categoria de Produto')
        verbose_name_plural = _('Categorias de Produtos')
        ordering = ['nome']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"


class Fornecedor(models.Model):
    TIPO_CHOICES = [
        ('F', 'Pessoa Física'),
        ('J', 'Pessoa Jurídica'),
    ]

    nome = models.CharField(max_length=100, verbose_name=_('Nome'))
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, verbose_name=_('Tipo'))
    cpf_cnpj = models.CharField(max_length=20, unique=True, verbose_name=_('CPF/CNPJ'), null=True, blank=True)
    email = models.EmailField(blank=True, null=True, verbose_name=_('E-mail'))
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Telefone'))
    observacoes = models.TextField(blank=True, null=True, verbose_name=_('Observações'))
    ativo = models.BooleanField(default=True, verbose_name=_('Ativo'))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Fornecedor')
        verbose_name_plural = _('Fornecedores')
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class LocalEstoque(models.Model):
    nome = models.CharField(max_length=100, verbose_name=_('Nome'))
    descricao = models.TextField(blank=True, null=True, verbose_name=_('Descrição'))
    responsavel = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Responsável'))
    ativo = models.BooleanField(default=True, verbose_name=_('Ativo'))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Local de Estoque')
        verbose_name_plural = _('Locais de Estoque')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    STATUS_CHOICES = [
        ('A', 'Ativo'),
        ('I', 'Inativo'),
        ('D', 'Descontinuado'),
    ]

    PERECIVEL_CHOICES = [
        ('S', 'Sim'),
        ('N', 'Não'),
        ('R', 'Refrigerado'),
        ('C', 'Congelado'),
    ]

    nome = models.CharField(max_length=100, verbose_name=_('Nome'))
    marca = models.CharField(max_length=100, verbose_name=_('Marca'), null=True, blank=True)
    descricao = models.TextField(blank=True, null=True, verbose_name=_('Descrição'))
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Categoria'))
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Fornecedor'))
    unidade_medida = models.CharField(max_length=3, choices=UNIDADE_CHOICES, default='UN', verbose_name=_('Unidade de Medida'))
    quantidade_atual = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[MinValueValidator(0)], verbose_name=_('Quantidade Atual'))
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Preço de Custo'))
    localizacao = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, related_name='produto', blank=True, null=True, verbose_name=_('Localização'))
    perecivel = models.CharField(max_length=1, choices=PERECIVEL_CHOICES, default='N')
    data_validade = models.DateField(blank=True, null=True)
    temperatura_conservacao = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A', verbose_name=_('Status'))
    foto = models.ImageField(upload_to='produtos/', blank=True, null=True, verbose_name=_('Foto'))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
        ordering = ['nome']

    def __str__(self):
        return f"{self.categoria} - {self.nome}"


class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
        ('A', 'Ajuste'),
        ('T', 'Transferência'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name=_('Produto'))
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, verbose_name=_('Tipo'))
    quantidade = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0.001)], verbose_name=_('Quantidade'))
    local_origem = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, related_name='movimentacoes_origem', blank=True, null=True, verbose_name=_('Local de Origem'))
    local_destino = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, related_name='movimentacoes_destino', blank=True, null=True, verbose_name=_('Local de Destino'))
    observacoes = models.TextField(blank=True, null=True, verbose_name=_('Observações'))
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Usuário'))
    data_movimentacao = models.DateTimeField(auto_now_add=True, verbose_name=_('Data da Movimentação'))
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name=_('Data de Atualização'))

    class Meta:
        verbose_name = _('Movimentação de Estoque')
        verbose_name_plural = _('Movimentações de Estoque')
        ordering = ['-data_movimentacao']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto} ({self.quantidade})"

    def save(self, *args, **kwargs):
        # Atualiza o estoque do produto quando uma movimentação é salva
        if not self.id:
            if self.tipo == 'E':
                self.produto.quantidade_atual += self.quantidade
            elif self.tipo == 'S':
                self.produto.quantidade_atual -= self.quantidade
            elif self.tipo == 'A':
                self.produto.localizacao = self.local_destino
            elif self.tipo == 'T':
                self.produto.localizacao = self.local_destino
        else:
            old_instance = MovimentacaoEstoque.objects.get(id=self.id)
            if old_instance.quantidade != self.quantidade:
                if self.tipo == 'E':
                    self.produto.quantidade_atual -= old_instance.quantidade
                    self.produto.quantidade_atual += self.quantidade
                elif self.tipo == 'S':
                    self.produto.quantidade_atual += old_instance.quantidade
                    self.produto.quantidade_atual -= self.quantidade
                elif self.tipo == 'A':
                    self.produto.localizacao = self.local_destino
                elif self.tipo == 'T':
                    self.produto.localizacao = self.local_destino
            else:
                if self.tipo == 'A':
                    self.produto.localizacao = self.local_destino
                elif self.tipo == 'T':
                    self.produto.localizacao = self.local_destino
        if self.tipo == 'S' and self.quantidade > self.produto.quantidade_atual:
            raise ValueError(
                f"Quantidade insuficiente em estoque. Disponível: {self.produto.quantidade_atual}"
            )
        self.produto.save()
        super().save(*args, **kwargs)


class Inventario(models.Model):
    STATUS_CHOICES = [
        ('A', 'Aberto'),
        ('F', 'Finalizado'),
        ('C', 'Cancelado'),
    ]

    local = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, verbose_name=_('Local'))
    data_inicio = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Início'))
    data_fim = models.DateTimeField(blank=True, null=True, verbose_name=_('Data de Fim'))
    responsavel = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Responsável'))
    observacoes = models.TextField(blank=True, null=True, verbose_name=_('Observações'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A', verbose_name=_('Status'))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Inventário')
        verbose_name_plural = _('Inventários')
        ordering = ['-data_inicio']

    def __str__(self):
        return f"Inventário {self.local} - {self.data_inicio.date()}"


class ItemInventario(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='itens', verbose_name=_('Inventário'))
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name=_('Produto'))
    quantidade_sistema = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_('Quantidade no Sistema'))
    quantidade_fisica = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_('Quantidade Física'))
    observacoes = models.TextField(blank=True, null=True, verbose_name=_('Observações'))
    conferido = models.BooleanField(default=False, verbose_name=_('Conferido'))
    data_conferencia = models.DateTimeField(blank=True, null=True, verbose_name=_('Data de Conferência'))
    usuario_conferencia = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Usuário Conferência'))

    class Meta:
        verbose_name = _('Item de Inventário')
        verbose_name_plural = _('Itens de Inventário')
        unique_together = ['inventario', 'produto']

    def __str__(self):
        return f"{self.produto} - Sistema: {self.quantidade_sistema} | Físico: {self.quantidade_fisica}"

    @property
    def diferenca(self):
        return self.quantidade_fisica - self.quantidade_sistema


class EnderecoFornecedor(models.Model):
    logadouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=100, null=True, blank=True)
    cliente = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Endereços do Fornecedor')
        verbose_name_plural = _('Endereços dos Fornecedores')

    def __str__(self):
        return f"{self.cliente}"


class EnderecoLocalEstoque(models.Model):
    logadouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=100, null=True, blank=True)
    estoque = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Endereços do Local de Estoque')
        verbose_name_plural = _('Endereços dos Locais de Estoque')

    def __str__(self):
        return f"{self.estoque}"
