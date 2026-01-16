from django.contrib.gis.db import models as geomodels # GeoDjango
from django.db import models
from core.models import User
from aircrafts.models import Aircraft

class OperationAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Inputs
    flight_height = models.FloatField(help_text="Altura de voo em metros")
    
    # Geometrias (Requer PostGIS)
    # Input do KML vira um Polígono aqui
    operational_volume = geomodels.PolygonField(srid=4326) 
    # Resultado do cálculo
    ground_risk_buffer = geomodels.PolygonField(srid=4326, blank=True, null=True)
    
    # Resultados da Análise
    is_populated = models.BooleanField(default=False)
    ibge_population_estimate = models.IntegerField(null=True, blank=True)
    sora_classification = models.CharField(max_length=50, blank=True) # Ex: "SAIL I", "SAIL II"

    def save(self, *args, **kwargs):
        # Lógica de automação: Ao salvar, se não tiver buffer, calcula.
        if not self.ground_risk_buffer and self.operational_volume:
            # 1. Calcular tamanho do buffer
            buffer_distance = self.aircraft.calculate_ground_risk_buffer(self.flight_height)
            
            # 2. Transformar projeção para metros (UTM ou WebMercator) para dar buffer
            # Nota: GeoDjango faz isso de forma elegante, mas requer projeção correta.
            # Este é um exemplo simplificado.
            self.ground_risk_buffer = self.operational_volume.buffer(buffer_distance / 111000) # Aproximação grosseira para graus, usaremos transformações reais no código final.
            
        super().save(*args, **kwargs)
