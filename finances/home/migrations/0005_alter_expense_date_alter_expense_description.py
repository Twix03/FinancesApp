# Generated by Django 4.2.3 on 2023-07-11 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_expense_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]