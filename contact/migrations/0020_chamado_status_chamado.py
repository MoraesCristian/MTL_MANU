# Generated by Django 5.1 on 2024-10-04 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0019_imagem_tipo_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='status_Chamado',
            field=models.CharField(choices=[('aberto', 'Aberto'), ('concluido', 'Concluído'), ('executando', 'Executando'), ('rejeitado', 'Rejeitado')], default='aberto', max_length=255),
        ),
    ]
