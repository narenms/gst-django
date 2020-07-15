from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    gstSlab = models.IntegerField()
    gstPrice = models.FloatField()
    