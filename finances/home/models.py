from django.db import models


# Create your models here.

class expense(models.Model):
    uid = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=15, decimal_places=3)
    description = models.CharField(max_length=255, null=True)
    date = models.DateField(null = True)
    category = models.CharField(max_length=255)
    file = models.FileField()


class income(models.Model):
    uid = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=15, decimal_places=3)
    description = models.CharField(max_length=255, null = True)
    date = models.DateField(null = True)
    category = models.CharField(max_length=255)
    file = models.FileField()

class category(models.Model):
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category