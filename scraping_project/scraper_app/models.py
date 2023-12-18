from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    image = models.URLField()

    def __str__(self):
        return self.name
