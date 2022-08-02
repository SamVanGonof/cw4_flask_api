from typing import Optional

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc, func
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorDAO(BaseDAO[Director]):
    __model__ = Director


class MovieDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None):
        """
        Получение всех фильмов, если status=new то вывод с новых фильмов

        :param page: Номер страницы
        :param status: настройка вывода фильмов
        """
        stmt: BaseQuery = self._db_session.query(self.__model__)

        if status == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UserDAO(BaseDAO[User]):
    __model__ = User

    def __init__(self, db_session) -> None:
        super().__init__(db_session)

    def get_by_email(self, email: str) -> User:
        """
        Получение пользователя по его логину
        """
        return self._db_session.query(self.__model__).filter(func.lower(self.__model__.email) == email).first()

    def add_user(self, data_user: dict) -> None:
        """
        Добавление нового пользователя

        :param data_user: данные пользователя
        """
        user = User(**data_user)
        self._db_session.add(user)
        self._db_session.commit()

    def update(self, user: User) -> None:
        """
        Обновление данных пользователя
        """
        self._db_session.add(user)
        self._db_session.commit()
