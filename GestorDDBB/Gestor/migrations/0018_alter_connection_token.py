# Generated by Django 5.0.14 on 2025-05-22 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestor', '0017_alter_connection_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='token',
            field=models.CharField(default='023792f0-58cb-4431-88d1-af9b76d8a069', max_length=256, unique=True),
        ),
    ]
