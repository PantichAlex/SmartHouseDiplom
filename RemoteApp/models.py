from django.db import models


class Users(models.Model):

    class Meta:
        db_table="Users"
        verbose_name="Пользователи"

    username=models.CharField(verbose_name="Пользователь", unique=True, max_length=50)
    email=models.EmailField(verbose_name="Эелектронная почта")
    phone=models.CharField(verbose_name="Телефон", max_length=20, null=True)



class Premissions(models.Model):

    class Meta:
        db_table="Permissions"
        verbose_name="Права"


class UserPemissions(models.Model):

    class Meta:
        db_table="UserPermissions"
        verbose_name="Права пользователей"

    user=models.ForeignKey(Users, on_delete=models.CASCADE)
    permission=models.ForeignKey(Premissions, on_delete=models.CASCADE)



class Devices(models.Model):

    class Meta:
        db_table="Devices"
        verbose_name="Устройства"

    name=models.CharField(verbose_name="Название", max_length=100)
    driverPath=models.CharField(verbose_name="Путь к драйверу", max_length=300)
    template=models.CharField(verbose_name="Шаблон интерфейса", max_length=300)


