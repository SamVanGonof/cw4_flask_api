import pytest

from project.dao import MovieDAO
from project.models import Movie


class TestMovies:
    @pytest.fixture
    def dao_movie(self, db):
        return MovieDAO(db.session)

    @pytest.fixture
    def movie2(self, db):
        item = Movie(title='movie2',
                     description='description2',
                     trailer='trailer2',
                     year=2000,
                     rating=2.2,
                     genre_id=2,
                     director_id=2)
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def movie1(self, db):
        item = Movie(title='movie1',
                     description='description1',
                     trailer='trailer1',
                     year=1000,
                     rating=1.1,
                     genre_id=1,
                     director_id=1)
        db.session.add(item)
        db.session.commit()
        return item

    def test_get_movie_by_id(self, movie1, dao_movie):
        assert dao_movie.get_by_id(movie1.id) == movie1

    def test_get_movie_by_id_not_found(self, dao_movie):
        assert not dao_movie.get_by_id(1)

    def test_get_all_movies(self, dao_movie, movie1, movie2):
        movies = dao_movie.get_all()
        assert movies == [movie1, movie2]
        assert movies != dao_movie.get_all(status='new')

    def test_get_movie_by_page(self, app, dao_movie, movie1, movie2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert dao_movie.get_all(page=1) == [movie1]
        assert dao_movie.get_all(page=2) == [movie2]
        assert dao_movie.get_all(page=3) == []


