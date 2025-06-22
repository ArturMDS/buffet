from django.db import models
from core.models import Funcionario


class Veiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=50, blank=True, null=True)
    odometro = models.IntegerField(default=0)
    ano_fabricacao = models.IntegerField(default=2000)
    chassi = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.marca} - {self.modelo}"


class RegistroMovimento(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data_saida = models.DateTimeField()
    odometro_saida = models.IntegerField(default=0)
    data_chegada = models.DateTimeField(null=True, blank=True)
    odometro_chegada = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.funcionario} ({self.veiculo}) - {self.data_saida}"

    def save(self, *args, **kwargs):
        self.veiculo.odometro = self.odometro_chegada
        self.veiculo.save()
        super().save(*args, **kwargs)
