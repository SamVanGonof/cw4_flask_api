from flask_restx import Namespace, Resource
from project.setup.api import user
from project.container import user_service
from project.setup.api.parsers import pr_passwords, pr_profile
from project.tools.decoration import authorizations

api = Namespace('user')


@api.route('/')
class UsersView(Resource):
    @api.response(404, "Нет пользователя с таким email")
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    @authorizations
    def get(self, email):
        """
        Получение пользователя по email

        :param email: email получаем в декораторе authorizations
        """
        return user_service.get_by_email(email=email)

    @api.response(500, 'Нет данных для изменения профиля')
    @api.expect(pr_profile)
    @authorizations
    def patch(self, email):
        """
        Изменение данных в профиле пользователя

        :param email: email получаем в декораторе authorizations
        """
        user_service.profile_update(email, pr_profile.parse_args())


@api.route('/password/')
class UserPasswordView(Resource):
    @api.response(500, 'Не введен новый или старый пароль')
    @api.expect(pr_passwords)
    @authorizations
    def put(self, email):
        """
        Изменение пароля пользователя

        :param email: email получаем в декораторе authorizations
        """
        user_service.password_update(email, pr_passwords.parse_args())
