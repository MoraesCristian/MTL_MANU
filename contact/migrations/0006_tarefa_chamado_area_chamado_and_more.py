# Generated by Django 5.1 on 2024-09-18 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_empresa_criado_por_alter_usuario_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(choices=[('Eletrica', 'Elétrica'), ('Hidraulica', 'Hidraulica'), ('Civil', 'Civil')], max_length=255)),
                ('descricao', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='chamado',
            name='area_chamado',
            field=models.CharField(choices=[('Eletrica', 'Elétrica'), ('Hidraulica', 'Hidraulica'), ('Civil', 'Civil')], default='Não especificado', max_length=255),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='tipo_manutencao',
            field=models.CharField(choices=[('preventiva', 'preventiva'), ('emergial', 'emergial'), ('corretiva', 'corretiva')], max_length=255),
        ),
        migrations.AddField(
            model_name='chamado',
            name='tarefa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contact.tarefa'),
        ),
    ]
