from django.db import models

class Aircraft(models.Model):
    name = models.CharField(max_length=100, verbose_name="Modelo da Aeronave")
    manufacturer = models.CharField(max_length=100, verbose_name="Fabricante")
    
    # Parâmetros SORA / Técnicos
    max_takeoff_weight = models.FloatField(help_text="MTOW em kg")
    max_speed = models.FloatField(help_text="Velocidade máxima em m/s")
    wingspan = models.FloatField(help_text="Envergadura em metros")
    
    # Parâmetros específicos para cálculo de Buffer (Simplificado)
    # Exemplo: Se o buffer é fixo por aeronave ou um multiplicador da altura
    buffer_ratio = models.FloatField(default=1.0, help_text="Multiplicador da altura (Ex: 1:1 = 1.0)")
    fixed_buffer_offset = models.FloatField(default=0.0, help_text="Margem fixa adicional em metros")

    def calculate_ground_risk_buffer(self, flight_height):
        """
        Lógica encapsulada: Retorna o tamanho do buffer em metros
        baseado na altura de voo e performance da aeronave.
        """
        # Aqui entra a lógica que você já possui.
        # Exemplo simples (Regra 1:1 + offset):
        return (flight_height * self.buffer_ratio) + self.fixed_buffer_offset

    def __str__(self):
        return f"{self.manufacturer} {self.name}"
