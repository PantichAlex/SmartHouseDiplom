from django.db import models

class Rooms(models.Model):
    class Meta:
        db_table="Rooms"
        verbose_name="Помещения"
        verbose_name_plural="Помещения"

    RoomName=models.CharField(verbose_name="Название", max_length=50)
    Description = models.CharField(verbose_name="Описание", max_length=500)

class Devices(models.Model):

    class Meta:
        db_table="Devices"
        verbose_name="Устройства"
        verbose_name_plural = "Устройства"

    name=models.CharField(verbose_name="Название", max_length=100)
    driverPath=models.CharField(verbose_name="Путь к драйверу", max_length=300)
    iconPath=models.CharField(verbose_name="Иконка", max_length=300)
    template=models.CharField(verbose_name="Шаблон интерфейса", max_length=300)
    room=models.ForeignKey(Rooms, verbose_name="Помещение", on_delete=models.CASCADE)

class Users(models.Model):

    class Meta:
        db_table="Users"
        verbose_name="Пользователи"
        verbose_name_plural = "Пользователи"

    username=models.CharField(verbose_name="Пользователь", unique=True, max_length=50)
    login=models.CharField(verbose_name="Логин", unique=True, max_length=45)
    password=models.CharField(verbose_name="Пароль", max_length=50)
    email=models.EmailField(verbose_name="Эелектронная почта")
    phone=models.CharField(verbose_name="Телефон", max_length=20, null=True)



class Premissions(models.Model):
    class Meta:
        db_table="Permissions"
        verbose_name="Права"
        verbose_name_plural = "Права"

    Description=models.CharField(verbose_name="Описание", max_length=500)
    device=models.ForeignKey(Devices, verbose_name="Устройство", on_delete=models.CASCADE)


class UserPemissions(models.Model):

    class Meta:
        db_table="UserPermissions"
        verbose_name="Права пользователей"
        verbose_name_plural = "Права пользователей"

    user=models.ForeignKey(Users, on_delete=models.CASCADE)
    permission=models.ForeignKey(Premissions, on_delete=models.CASCADE)


class Macro(models.Model):
    class Meta:
        db_table="Macro"
        verbose_name="Пользовательские макросы"
        verbose_name_plural="Пользовательские макросы"

    user=models.ForeignKey(Users,on_delete=models.CASCADE,verbose_name="Пользователь")
    device=models.ForeignKey(Devices, on_delete=models.CASCADE, verbose_name="Устройство")
    text=models.CharField(verbose_name="Текст макроса", max_length=1000)