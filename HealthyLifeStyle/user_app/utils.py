from django.core.mail import send_mail
from django.conf import settings
from .smsc_api import SMSC


def send_verification_code_email(email, code):
    send_mail(
        'ЗОЖНИК. Код верификации',
        f'Ваш код для верификации: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def send_verification_code_sms(phone, code):
    smsc = SMSC()
    message = f'Ваш код для верификации: {code}'
    smsc.send_sms(phone, message)
