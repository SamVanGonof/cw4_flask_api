from typing import Optional

from project.dao import MovieDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MoviesService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        """
        Получение фильма по id

        :param pk: id фильма
        """
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Director with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> list[Movie]:
        """
        Получение всех фильмов
        """
        return self.dao.get_all(page=page, status=status)
