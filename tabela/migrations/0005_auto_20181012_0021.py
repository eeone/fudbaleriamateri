# Generated by Django 2.1.2 on 2018-10-11 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabela', '0004_auto_20181012_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
