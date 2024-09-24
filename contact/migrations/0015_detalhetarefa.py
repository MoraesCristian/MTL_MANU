# Generated by Django 5.1 on 2024-09-24 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0014_alter_mensagemchat_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalheTarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalhes', to='contact.tarefa')),
            ],
        ),
    ]
