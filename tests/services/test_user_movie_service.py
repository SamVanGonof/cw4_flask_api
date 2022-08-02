from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.models import User, Movie
from project.services import UserMovieService


class TestUserMovieService:
    @pytest.fixture
    def movie1(self):
        item = Movie(id=1,
                     title='movie1',
                     description='description1',
                     trailer='trailer1',
                     year=1000,
                     rating=1.1,
                     genre_id=1,
                     director_id=1)
        return item

    @pytest.fixture
    def movie2(self):
        item = Movie(id=2,
                     title='movie2',
                     description='description2',
                     trailer='trailer2',
                     year=2000,
                     rating=2.2,
                     genre_id=2,
                     director_id=2)
        return item

    @pytest.fixture
    @patch('project.dao.MovieDAO')
    def movie_dao_moc(self, moc_dao, movie1, movie2):
        dao = moc_dao()
        dao.get_by_id.return_value = movie1
        dao.get_all.return_value = [movie1, movie2]
        return dao

    @pytest.fixture
    @patch('project.dao.UserDAO')
    def user_dao_moc(self, moc_dao, movie1, movie2):
        dao = moc_dao()
        dao.get_by_email.return_value = User(id=1,
                                             email='email1',
                                             password='hash_password',
                                             name='name1',
                                             surname='surname1',
                                             favorite_genre_id=1,
                                             movie_favorites=[movie1, movie2])
        return dao

    @pytest.fixture
    def user_movie_service(self, user_dao_moc, movie_dao_moc):
        return UserMovieService(dao_user=user_dao_moc, dao_movie=movie_dao_moc)

    def test_get_all_by_uid(self, user_movie_service, user_dao_moc):
        item = user_movie_service.get_all_by_uid('email1')
        user = user_dao_moc.get_by_email.return_value
        assert item == user.movie_favorites
        assert len(item) == 2

    def test_get_all_by_uid_raise(self, user_movie_service, user_dao_moc):
        user_dao_moc.get_by_email.return_value = None
        with pytest.raises(ItemNotFound):
            user_movie_service.get_all_by_uid('email')

    def test_add_movie(self, user_movie_service):
        user_movie_service.add_movie('email', 1)

    def test_add_movie_raise(self, user_movie_service, user_dao_moc, movie_dao_moc):
        user_dao_moc.get_by_email.return_value = None
        movie_dao_moc.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            user_movie_service.add_movie('email', 1)

    def test_delete_movie(self, user_movie_service):
        user_movie_service.delete_movie('email', 1)

    def test_delete_movie_raise(self, user_movie_service, user_dao_moc, movie_dao_moc):
        user_dao_moc.get_by_email.return_value = None
        movie_dao_moc.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            user_movie_service.delete_movie('email', 1)




