# Generated by Django 5.1 on 2024-09-20 02:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0009_alter_area_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='descricao',
        ),
        migrations.AlterField(
            model_name='area',
            name='nome',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='area_chamado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contact.area'),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.area'),
        ),
    ]