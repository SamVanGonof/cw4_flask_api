import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import current_app, abort


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    """
    Генератор хеш пароль

    :param password: хэшируемый пароль
    """
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compose_passwords(password1: str, password2: str) -> bool:
    """
    Проверка двух паролей
    :param password1: пароль1
    :param password2: пароль2
    """
    return hmac.compare_digest(password1, password2)


def decode_token(token: str) -> dict:
    """
    Декодировка полученного токена
    """
    data_user = None
    try:
        data_user = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except Exception as e:
        print('JWT Decode Error', e)
        abort(401)

    return data_user


def generate_token(data_user: dict) -> dict:
    """
    Генератор пары токенов access_token и refresh_token
    """
    minutes = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data_user['exp'] = calendar.timegm(minutes.timetuple())
    access_token = jwt.encode(data_user, key=current_app.config['SECRET_KEY'], algorithm='HS256')

    days = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
    data_user['exp'] = calendar.timegm(days.timetuple())
    refresh_token = jwt.encode(data_user, key=current_app.config['SECRET_KEY'], algorithm='HS256')

    return {'access_token': access_token, 'refresh_token': refresh_token}

