# Generated by Django 4.0.4 on 2022-06-01 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brasileiro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadio',
            name='capacidade',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='estadio',
            name='nomeCompleto',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='jogador',
            name='dtnasc',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='jogador',
            name='nomeCompleto',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='apelido',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='nomeCompleto',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
