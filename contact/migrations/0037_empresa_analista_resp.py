# Generated by Django 5.1.4 on 2025-01-22 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0036_usuario_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='analista_resp',
            field=models.ForeignKey(blank=True, limit_choices_to={'tipo_usuario': 'operador'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='empresas_responsaveis', to=settings.AUTH_USER_MODEL),
        ),
    ]
