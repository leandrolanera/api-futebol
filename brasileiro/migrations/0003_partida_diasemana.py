# Generated by Django 4.0.4 on 2022-06-04 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brasileiro', '0002_alter_estadio_capacidade_alter_estadio_nomecompleto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='diaSemana',
            field=models.CharField(max_length=30, null=True),
        ),
    ]