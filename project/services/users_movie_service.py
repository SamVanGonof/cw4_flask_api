from project.dao.main import UserDAO, MovieDAO
from project.exceptions import ItemNotFound
from project.models import User, Movie


class UserMovieService:
    def __init__(self, dao_user: UserDAO, dao_movie: MovieDAO):
        self.dao_user = dao_user
        self.dao_movie = dao_movie

    def get_all_by_uid(self, email: str) -> list[User]:
        """
        Получение всех избранных фильмов пользователя.

        :param email: email пользователя
        """
        items = self.dao_user.get_by_email(email)  # получаем пользователя по email
        if items:
            return items.movie_favorites  # передаем его фильмы
        else:
            raise ItemNotFound('Нет избранных файлов')

    def add_movie(self, email: str, mid: int) -> None:
        """
        Добавление фильма в избранное к пользователю по id

        :param email: email пользователя
        :param mid: id фильма
        """

        user: User = self.dao_user.get_by_email(email)
        movie: Movie = self.dao_movie.get_by_id(mid)

        if not user or not movie:
            raise ItemNotFound('Нет избранных файлов')

        user.movie_favorites.append(movie)  # добавление фильма в избранного пользователя
        self.dao_user.update(user)

    def delete_movie(self, email: str, mid: int) -> None:
        """
        Удаление фильма из избранного у пользователя

        :param email: email пользователя
        :param mid: id фильма
        """

        user: User = self.dao_user.get_by_email(email)
        movie: Movie = self.dao_movie.get_by_id(mid)

        if not user or not movie:
            raise ItemNotFound('Нет избранных файлов')

        user.movie_favorites.remove(movie)  # удаление фильма из избранного пользователя
        self.dao_user.update(user)
