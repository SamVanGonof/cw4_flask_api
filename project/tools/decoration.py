from flask import request, abort

from project.tools.security import decode_token


def authorizations(func):
    """
    Декоратор для проверки токена и передачи email в декорируемую функцию
    """
    def wrapper(*args, **kwargs):
        access_token = request.cookies.get('AccessToken')

        if not access_token:
            abort(401)

        data = decode_token(access_token)

        return func(*args, **kwargs, email=data['email'])

    return wrapper
