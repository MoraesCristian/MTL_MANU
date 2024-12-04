# Generated by Django 5.1 on 2024-11-24 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0032_chamado_data_limite_atendimento_tempomanutencao'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(choices=[('financeiro', 'Financeiro'), ('contrato', 'Contrato')], max_length=50)),
                ('descricao', models.CharField(blank=True, max_length=255, null=True)),
                ('documento', models.FileField(upload_to='documentos_empresa/')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='contact.empresa')),
            ],
        ),
    ]
