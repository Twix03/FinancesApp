# Generated by Django 4.2.3 on 2023-07-11 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_expense_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='uid',
            field=models.IntegerField(default=0, max_length=10000),
        ),
        migrations.AddField(
            model_name='income',
            name='uid',
            field=models.IntegerField(default=0, max_length=10000),
        ),
    ]
