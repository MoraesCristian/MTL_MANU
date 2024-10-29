# Generated by Django 5.1 on 2024-10-29 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0026_imagemchamado_data_upload_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagemchat',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='imagens_chat/'),
        ),
        migrations.AlterField(
            model_name='mensagemchat',
            name='conteudo',
            field=models.TextField(blank=True),
        ),
    ]
