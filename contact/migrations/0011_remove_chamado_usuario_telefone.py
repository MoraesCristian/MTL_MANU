# Generated by Django 5.1 on 2024-09-20 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0010_remove_area_descricao_alter_area_nome_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chamado',
            name='usuario_telefone',
        ),
    ]
