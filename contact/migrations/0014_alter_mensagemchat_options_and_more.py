# Generated by Django 5.1 on 2024-09-24 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0013_chat_mensagemchat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mensagemchat',
            options={},
        ),
        migrations.RenameField(
            model_name='mensagemchat',
            old_name='mensagem',
            new_name='conteudo',
        ),
    ]
