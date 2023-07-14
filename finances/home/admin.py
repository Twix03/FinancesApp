from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.income)
admin.site.register(models.expense)
admin.site.register(models.category)