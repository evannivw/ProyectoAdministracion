from django.db import models

# Create your models here.
class MonthlyWeatherByCity(models.Model):
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)


class Registrado(models.Model):
    nombre = models.CharField(max_length=100, blank=True,null=True)
    email = models.EmailField()
    timeStamp = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.email