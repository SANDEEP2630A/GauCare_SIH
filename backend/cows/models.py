from django.db import models


class Cow(models.Model):
    cow_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cow_id
class Scan(models.Model):
    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="scans"
    )

    scan_number = models.PositiveIntegerField()
    day = models.PositiveIntegerField()

    # Milk / sensor measurements
    conductivity_raw_mScm = models.FloatField()
    temperature_C = models.FloatField()
    conductivity_temp_adjusted_mScm = models.FloatField()
    milk_pH = models.FloatField()
    somatic_cell_count = models.FloatField()
    milk_yield_L = models.FloatField()
    clotting = models.BooleanField(default=False)

    # AS7343 spectral channels
    as7343_F1 = models.FloatField()
    as7343_F2 = models.FloatField()
    as7343_FZ = models.FloatField()
    as7343_F3 = models.FloatField()
    as7343_F4 = models.FloatField()
    as7343_F5 = models.FloatField()
    as7343_FY = models.FloatField()
    as7343_FXL = models.FloatField()
    as7343_F6 = models.FloatField()
    as7343_F7 = models.FloatField()
    as7343_F8 = models.FloatField()
    as7343_NIR = models.FloatField()
    as7343_VIS = models.FloatField()
    as7343_FD = models.FloatField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cow.cow_id} - Scan {self.scan_number}"
class Prediction(models.Model):
    scan = models.OneToOneField(
        Scan,
        on_delete=models.CASCADE,
        related_name="prediction"
    )

    risk_score = models.FloatField()
    risk_label = models.CharField(max_length=20)

    model_version = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.scan} - {self.risk_label}"
# Create your models here.
