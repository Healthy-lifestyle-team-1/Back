from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def custom_validation(data):
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    password = data['password'].strip()

    if not email and not phone:
        raise ValidationError('Необходимо ввести номер телефона или email')
    if email and UserModel.objects.filter(email=email).exists():
        raise ValidationError('Email уже используется')
    if phone and UserModel.objects.filter(phone=phone).exists():
        raise ValidationError('Номер телефона уже используется')
    if not password or len(password) < 8:
        raise ValidationError('Выберите другой пароль, не менее 8 символов')
    return data


def validate_login(data):
    login = data.get('login', '').strip()
    if not login:
        raise ValidationError('Необходимо ввести номер телефона или email')
    return True


def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('Необходимо ввести пароль')
    return True
