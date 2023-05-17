from django.core.mail import send_mail
from dating_and_matches.settings import EMAIL_HOST_USER


def send_register(email, password):
    """
    Sends a registration email to the specified email address.

    Args:
        email (str): The recipient's email address.
        password (str): The generated password for the user.

    Returns:
        None

    Raises:
        None
    """
    send_mail(
        'You have successfully registered on the DATING AND MATCHES website! Welcome.',
        f'Your login is {email}, and your password is {password}. We strongly recommend you to prevent third parties from accessing it.',
        EMAIL_HOST_USER,
        [email],
        fail_silently=True
    )
