from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.models import Movie
from project.services import MoviesService


class TestMovieService:
    @pytest.fixture
    def movie1(self, db):
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
    def movie2(self, db):
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
    def service_movie(self, movie_dao_moc):
        return MoviesService(dao=movie_dao_moc)

    @pytest.fixture
    def movie(self, db):
        item = Movie(title='movie',
                     description='description',
                     trailer='trailer',
                     year=2000,
                     rating=2.2,
                     genre_id=2,
                     director_id=2)
        db.session.add(item)
        db.session.commit()
        return item

    def test_get_movie_by_id(self, movie, service_movie):
        assert service_movie.get_item(movie.id)

    def test_movie_not_found(self, movie_dao_moc, service_movie):
        movie_dao_moc.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            service_movie.get_item(10)

    @pytest.mark.parametrize('page, status', ([1, None], ['new', 'new']), ids=['with page', 'without page'])
    def test_get_genres(self, movie_dao_moc, service_movie, page: int | None, status: str):
        movie = service_movie.get_all(page=page, status=status)
        assert len(movie) == 2
        assert movie == movie_dao_moc.get_all.return_value
        movie_dao_moc.get_all.assert_called_with(page=page, status=status)

