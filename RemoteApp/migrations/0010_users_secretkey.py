# Generated by Django 2.1.7 on 2019-06-20 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RemoteApp', '0009_devices_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='secretKey',
            field=models.CharField(max_length=50, null=True, verbose_name='Секретный ключ'),
        ),
    ]