from ctypes import CDLL, c_int, c_char_p
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.db import models
from django.core.exceptions import PermissionDenied
from hashlib import sha256,sha512,md5
from random import randint,choice
from config import login as eLogin ,password as ePassword
import smtplib

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
    deleted=models.BooleanField(verbose_name="Удален", default=False)

    def __str__(self):

        return self.name

class Premissions(models.Model):
    class Meta:
        db_table="Permissions"
        verbose_name="Права"
        verbose_name_plural = "Права"

    Description=models.CharField(verbose_name="Описание", max_length=500)
    device=models.ForeignKey(Devices, verbose_name="Устройство", on_delete=models.CASCADE)
    read=models.BooleanField(verbose_name="Право на чтение", default=False)
    write=models.BooleanField(verbose_name="Право на отправку команды",default=False)

    def __str__(self):
        return self.Description



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
    token=models.CharField(verbose_name="Уникальнай токен", max_length=200, null=True, unique=True)
    refreshToken=models.CharField(verbose_name="Токен обновления", max_length=200, null=True, unique=True)
    secretKey=models.CharField(verbose_name="Секретный ключ", max_length=50, null=True)
    deleted=models.BooleanField(verbose_name="Удален", default=False)
    admin = models.BooleanField(verbose_name="Администратор", default=False)
    permissions=models.ManyToManyField(Premissions, verbose_name="Права")


    def __str__(self):
        return self.username

    def generateTokens(self):
        num1 = randint(1, 100000)
        num2 = randint(1, 100000)
        basestr = self.login + self.password
        str1 = bytes(basestr.join(str(num1)), encoding='utf-8')
        str2 = bytes(basestr.join(str(num2)), encoding='utf-8')

        self.token = sha256(str1).hexdigest()
        self.refreshToken = sha512(str2).hexdigest()
        self.save()

    def resetTokens(self, refreshToken):
        if(self.refreshToken==refreshToken):
            self.generateTokens()
        else:
            raise PermissionDenied()


    def correctPassword(self, password):
        password=md5(bytes(password,encoding='utf-8')).hexdigest()
        return password==self.password

    def changePassword(self, password, newPassword):
        if(not self.correctPassword(password)):
            raise PermissionDenied()

        self.password=md5(bytes(newPassword, encoding="utf-8")).hexdigest()
        self.generateTokens()

        self.save()

    def resetPassword(self):
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        password=""
        while(len(password)<8):
            password+=choice(chars)

        message="Ваш пароль был сброшен зпросом на сброс. Ваш новый пароль: %s" % password

        try:
            msg=MIMEMultipart()
            msg['From']=eLogin
            msg['To']=self.email
            msg['Subject']="Сброс пароля"
            msg.attach(MIMEText(message))
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(eLogin,ePassword)
            smtpObj.sendmail(msg['From'],msg['To'], msg.as_string())

        finally:
            smtpObj.quit()

        self.password = md5(bytes(password, encoding="utf-8")).hexdigest()
        self.generateTokens()



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

    typeName=models.CharField(verbose_name="Тип", max_length=20, unique=True)
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
    driverIdenti=models.CharField(verbose_name="имя команды внутри драйвера", max_length=50, default="")
    value=models.IntegerField(verbose_name="Значение")
    minValue=models.IntegerField(verbose_name="Минимальное значение", null=True)
    maxValue=models.IntegerField(verbose_name="Максимальное значение", null=True)
    description=models.CharField(verbose_name="Описание команды", max_length=255)

    def __str__(self):
        return self.name

    def setValue(self,value):
        if(self.minValue>value or self.maxValue<value):
            return False;
        driverPath=self.device.driverPath

        dll=CDLL(driverPath)
        command=c_char_p(self.driverIdenti.encode('utf-8'))
        cvalue=c_int(value)
        dll.sendCommand(command,value)
        self.value=value
        self.save()

        return True
