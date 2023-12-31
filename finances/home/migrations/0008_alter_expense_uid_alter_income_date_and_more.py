# Generated by Django 4.2.3 on 2023-07-12 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_category_expense_uid_income_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='uid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='uid',
            field=models.IntegerField(),
        ),
    ]
