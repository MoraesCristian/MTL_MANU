# Generated by Django 5.1.4 on 2025-01-22 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0035_empresa_email_responsavel_empresa_responsavel_empre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
