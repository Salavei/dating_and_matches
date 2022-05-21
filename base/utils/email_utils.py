# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/4/24 16:35'

from django.core.mail import send_mail
from ..models import EmailVeriRecord
import random
import datetime
from dating_and_matches import settings
from datetime import timedelta


# Произвольно сгенерировать код проверки функции
def random_codechr(length=16):
    # Код подтверждения случайной комбинации регистра
    chars = 'quFDGDbtwehykjahuhufHFCUHNCWEHAFDONCJUHU'
    codechr = ''
    for x in range(length):
        # Случайно вытащить персонажа
        codechr += random.choice(chars)
    return codechr


#
def send_email(to_email, send_type='app'):
    """
         : param to_email: адрес электронной почты получателя
         : param send_type: тип почты
         : return: Результат отправки электронного письма
    """
    email = EmailVeriRecord()
    # получить код подтверждения
    email.code = random_codechr()
    # Получатель
    email.email = to_email
    # Срок действия
    email.exprie_time = datetime.datetime.now() + datetime.timedelta(days=7)
    # Тип почты
    email.send_type = send_type
    # отправить электронное письмо
    try:
        res = send_mail('Электронный адрес активации форума', '', settings.EMAIL_HOST_USER, [to_email],
                        html_message='Добро пожаловать, чтобы зарегистрироваться на форуме, нажмите ссылку для активации своей учетной записи: <a href = "127.0.0.1:8000/active/ {} "> 127.0.0.1:8000/active/ {} </a> '.format(
                            email.code, email.code))
        if res == 1:
            # Сохранить записи электронной почты
            email.save()
            return True
        else:
            return False
    except EmailVeriRecord as e:
        print(e)
    return False

