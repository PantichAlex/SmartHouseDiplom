# Generated by Django 2.1.7 on 2019-06-21 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RemoteApp', '0015_auto_20190621_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandtype',
            name='typeName',
            field=models.CharField(max_length=20, unique=True, verbose_name='Тип'),
        ),
    ]