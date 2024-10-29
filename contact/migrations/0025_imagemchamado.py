# Generated by Django 5.1 on 2024-10-28 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0024_empresa_filial_de'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemChamado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='fotos_chamados/')),
                ('chamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.chamado')),
            ],
        ),
    ]