from django.db import models
from django.contrib.auth.models import AbstractUser
from aircrafts.models import Aircraft

class Company(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, blank=True)
    
    # A Mágica da restrição acontece aqui:
    # Uma empresa tem acesso a muitas aeronaves, e uma aeronave serve a muitas empresas.
    authorized_aircrafts = models.ManyToManyField(Aircraft, related_name='authorized_companies')

    def __str__(self):
        return self.name

class User(AbstractUser):
    # Linkamos o usuário (piloto/gestor) a uma empresa
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
