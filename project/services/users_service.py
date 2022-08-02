import string
from typing import Any, Dict

from project.dao import UserDAO
from project.exceptions import ItemNotFound, BaseServiceError
from project.models import User
from project.tools.security import generate_password_hash, compose_passwords, generate_token, decode_token


class UserService:
    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_by_email(self, email: str) -> User:
        """
        Получение пользователя по его логину
        """
        if user := self.dao.get_by_email(email.lower()):
            return user
        else:
            raise ItemNotFound("Нет пользователя с таким email")

    def profile_update(self, email: str, data_profile: Dict[str, Any]) -> None:
        """
        Изменение или добавление данных профиля пользователя

        :param email: email пользователя
        :param data_profile: данные для изменения профиля
        """
        if not any(data_profile.values()):  # если нет данных для изменения профиля, то вызываем ошибку
            raise BaseServiceError('Нет данных')

        user = self.get_by_email(email)

        if name := data_profile.get('name'):
            user.name = name
        if surname := data_profile.get('surname'):
            user.surname = surname
        if favourite_genre := data_profile.get('favourite_genre'):
            user.favorite_genre_id = favourite_genre

        self.dao.update(user)

    def password_update(self, email: str, data: dict) -> None:
        """
        Изменение пароля пользователя
        :param email: email пользователя
        :param data: данные для изменения парола пользователя
        """
        if not all(data.values()):  # если нет какого нибудь значения, то вызываем ошибку
            raise BaseServiceError('Нет данных')

        user = self.get_by_email(email)

        hash_password = generate_password_hash(data.get('old_password'))

        if compose_passwords(hash_password, user.password):
            user.password = generate_password_hash(data.get('new_password'))

        self.dao.update(user)

    def add_user(self, data_user: dict) -> None:
        """
        Регистрация нового пользователя

        :param data_user: данные для создания пользователя
        """
        if all(data_user.values()):  # если какого нибудь значения нет вызываем ошибку
            data_user['password'] = generate_password_hash(data_user.get('password'))  # хэшируем пароль
            self.dao.add_user(data_user)
        else:
            raise BaseServiceError('Не введен логин или пароль')

    def user_password_verification(self, data_user: dict) -> dict:
        """
        Авторизация пользователя и получения токенов
        :param data_user: email и пароль
        """
        if not all(data_user.values()):
            raise BaseServiceError('Не введен логин или пароль')

        user = self.get_by_email(data_user.get('email'))
        data = {'email': user.email,
                'password': user.password}

        if compose_passwords(generate_password_hash(data_user['password']), user.password):  # Проверка пароля
            return generate_token(data)
        else:
            raise BaseServiceError("Неправильный пароль")

    def generate_new_token(self, token: str) -> dict:
        """
        Генерация новой пары токенов, по refresh_token
        :param token: refresh_token
        """
        if not token:
            raise BaseServiceError("Нет токена")

        data = decode_token(token)
        user = self.get_by_email(data['email'])

        if compose_passwords(data['password'], user.password):
            return generate_token(data)
        else:
            raise BaseServiceError()
