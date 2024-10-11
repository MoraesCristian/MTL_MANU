# Generated by Django 5.1 on 2024-10-01 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0016_detalhetarefapreenchido_delete_imagemchamado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='tarefa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chamados', to='contact.tarefa'),
        ),
    ]
