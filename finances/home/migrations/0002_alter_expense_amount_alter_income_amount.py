# Generated by Django 4.2.3 on 2023-07-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=3, max_digits=15),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=3, max_digits=15),
        ),
    ]
