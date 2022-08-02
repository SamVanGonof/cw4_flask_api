from flask_restx import Namespace, Resource
from project.setup.api import movie
from project.tools.decoration import authorizations
from project.container import user_movie_service

api = Namespace('favorites')


@api.route('/movies/')
class FavoritesView(Resource):
    @api.response(404, 'Нет избранных файлов')
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    @authorizations
    def get(self, email):
        """
        Получение избранных фильмов пользователя

        :param email: получаем в authorizations
        """
        return user_movie_service.get_all_by_uid(email)


@api.route('/movies/<int:movie_id>/')
class FavoriteView(Resource):
    @api.response(404, 'Нет избранных файлов')
    @authorizations
    def post(self, movie_id, email):
        """
        Добавление фильма в избранное пользователя

        :param movie_id: id фильма
        :param email: email получаем в authorizations
        """
        user_movie_service.add_movie(email, movie_id)

    @api.response(404, 'Нет избранных файлов')
    @authorizations
    def delete(self, movie_id, email):
        """
        Удаление фильма из избранного пользователя

        :param movie_id: id фильма
        :param email: email получаем из authorizations
        """
        user_movie_service.delete_movie(email, movie_id)
