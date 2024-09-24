# Generated by Django 5.1 on 2024-09-23 17:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0012_remove_chamado_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chamado', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='contact.chamado')),
            ],
        ),
        migrations.CreateModel(
            name='MensagemChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.TextField()),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensagens', to='contact.chat')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['data_envio'],
            },
        ),
    ]