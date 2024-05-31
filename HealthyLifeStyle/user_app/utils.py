from django.core.mail import send_mail
from django.conf import settings


def send_verification_code_email(email, code):
    send_mail(
        'Your verification code',
        f'Your verification code is {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def send_verification_code_sms(phone, code):
    # Здесь будет код для отправки SMS через сервис отправки сообщений.
    # Пример с использованием Twilio:
    # from twilio.rest import Client
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=f'Your verification code is {code}',
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=phone
    # )
    pass
