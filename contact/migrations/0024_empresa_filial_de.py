# Generated by Django 5.1 on 2024-10-21 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0023_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='filial_de',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='filiais', to='contact.empresa'),
        ),
    ]