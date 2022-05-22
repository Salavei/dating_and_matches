from django.core.mail import send_mail
from dating_and_matches.settings import EMAIL_HOST_USER


def send_register(email, password):
    send_mail(
        'Вы успешно зарегестировались на сайте DATING AND MATCHES! Добро пожаловать',
        f'Ваш логин {email} , пароль {password} . Настоятельно Вам рекомендуем предотвращать попаданию третьим лицам',
        f'{EMAIL_HOST_USER}',
        [email], fail_silently=False)
