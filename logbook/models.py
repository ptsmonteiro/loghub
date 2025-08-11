from django.db import models


class Upload(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Upload {self.pk}"


class QSO(models.Model):
    upload = models.ForeignKey(Upload, related_name="qsos", on_delete=models.CASCADE)
    call = models.CharField(max_length=32)
    station_callsign = models.CharField(max_length=32)
    qso_date = models.DateField(null=True, blank=True)
    time_on = models.TimeField(null=True, blank=True)
    freq = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    band = models.CharField(max_length=16, blank=True)
    mode = models.CharField(max_length=16, blank=True)

    def __str__(self) -> str:
        return f"{self.call} @ {self.qso_date} {self.time_on}"
