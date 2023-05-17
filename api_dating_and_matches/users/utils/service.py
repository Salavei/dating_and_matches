from django.core.mail import send_mail
from dating_api.settings import EMAIL_HOST_USER


def send_message__about_register(email, password):
    send_mail(
        'You have successfully registered on the DATING AND MATCHES website! Welcome',
        f'Your login: {email}, password: {password}. We strongly recommend preventing third-party access.',
        f'{EMAIL_HOST_USER}',
        [email],
        fail_silently=True
    )
