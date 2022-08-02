from flask_restx import Namespace, Resource
from project.setup.api import pr_user, pr_refresh_token
from project.container import user_service

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @api.response(500, 'Не введен логин или пароль')
    @api.expect(pr_user)
    def post(self):
        """
        Регистрация нового пользователя
        """
        user_service.add_user(pr_user.parse_args())


@api.route('/login/')
class AuthsView(Resource):
    @api.response(500, "Не введен логин или пароль или Неправильный пароль")
    @api.expect(pr_user)
    def post(self):
        """
        Получение пары токенов после авторизации
        """
        return user_service.user_password_verification(pr_user.parse_args())

    @api.response(500, "Не введен токен")
    @api.expect(pr_refresh_token)
    def put(self):
        """
        Получение пары токенов по refresh_token
        """
        return user_service.generate_new_token(pr_refresh_token.parse_args().get('RefreshToken'))
