# Generated by Django 5.1.3 on 2025-01-23 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folder_aplikacji', '0002_przepis_kategoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='przepis',
            name='czas_przygotowania',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='przepis',
            name='kategoria',
            field=models.CharField(max_length=100),
        ),
    ]
