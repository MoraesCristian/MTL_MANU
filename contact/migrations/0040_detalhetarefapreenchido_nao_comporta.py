# Generated by Django 5.1.4 on 2025-02-19 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0039_remove_empresa_analista_resp_chamado_analista_resp'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalhetarefapreenchido',
            name='nao_comporta',
            field=models.BooleanField(default=False),
        ),
    ]
