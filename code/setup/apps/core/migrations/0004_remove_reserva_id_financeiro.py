# Generated by Django 5.2 on 2025-06-19 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_reserva_id_hospede_alter_reserva_id_quarto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='id_financeiro',
        ),
    ]
