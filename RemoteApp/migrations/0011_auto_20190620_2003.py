# Generated by Django 2.1.7 on 2019-06-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RemoteApp', '0010_users_secretkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='premissions',
            name='read',
            field=models.BooleanField(default=False, verbose_name='Право на чтение'),
        ),
        migrations.AddField(
            model_name='premissions',
            name='write',
            field=models.BooleanField(default=False, verbose_name='Право на отправку команды'),
        ),
    ]
