# Generated by Django 5.1 on 2024-10-31 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0027_mensagemchat_imagem_alter_mensagemchat_conteudo'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='assinatura',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='email_assinante',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='chamado',
            name='nome_assinante',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
