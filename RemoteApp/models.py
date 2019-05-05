from django.db import models
from hashlib import sha256

class Rooms(models.Model):
    class Meta:
        db_table="Rooms"
        verbose_name="Помещения"
        verbose_name_plural="Помещения"

    RoomName=models.CharField(verbose_name="Название", max_length=50)
    Description = models.CharField(verbose_name="Описание", max_length=500)

    def __str__(self):
        return self.RoomName

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

    def __str__(self):

        return self.name

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
    token=models.CharField(verbose_name="Уникальнай токен", max_length=200, null=True)


    def __str__(self):
        return self.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        st=bytes(self.login+self.password, encoding='utf-8')
        self.token=sha256(st).hexdigest()
        super().save(force_insert, force_update, using, update_fields)


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


class CommandType(models.Model):
    class Meta:
        db_table="CommandType"
        verbose_name="Тип команды"
        verbose_name_plural="Типы команд"

    typeName=models.CharField(verbose_name="Тип", max_length=20)
    desMax=models.IntegerField(verbose_name="Критическое максимальное значение")
    desMin=models.IntegerField(verbose_name="Критическое минимальное значение")
    def __str__(self):
        return self.typeName

class Command(models.Model):
    class Meta:
        db_table="Command"
        verbose_name="Команда"
        verbose_name_plural="Команды"

    name=models.CharField(verbose_name="Название команды", max_length=30)
    ctype=models.ForeignKey(CommandType, on_delete=models.CASCADE, verbose_name="Тип команды")
    device=models.ForeignKey(Devices, on_delete=models.CASCADE,verbose_name="Устройство")
    value=models.IntegerField(verbose_name="Значение")
    minValue=models.IntegerField(verbose_name="Минимальное значение", null=True)
    maxValue=models.IntegerField(verbose_name="Максимальное значение", null=True)
    description=models.CharField(verbose_name="Описание команды", max_length=255)

    def __str__(self):
        return self.name

    def setValue(self,value):
        if(self.minValue>value or self.maxValue<value):
            return False;

        self.value=value
        self.save()
        return True