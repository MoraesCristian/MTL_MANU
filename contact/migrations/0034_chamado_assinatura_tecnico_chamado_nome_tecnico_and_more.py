# Generated by Django 5.1 on 2024-12-11 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0033_documentoempresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='assinatura_tecnico',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='nome_tecnico',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='status_chamado',
            field=models.CharField(choices=[('aberto', 'Aberto'), ('concluido', 'Concluído'), ('executando', 'Executando'), ('rejeitado', 'Rejeitado'), ('assinatura', 'Aguardando assinatura'), ('vencidas', 'OS Vencida')], default='aberto', max_length=255),
        ),
    ]
