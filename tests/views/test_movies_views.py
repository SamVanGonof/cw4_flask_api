import pytest

from project.models import Movie, Genre, Director


class TestMoviesViews:
    @pytest.fixture
    def genre(self, db):
        item = Genre(name='genre')
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def director(self, db):
        item = Director(name='director')
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def movie(self, db):
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

    @pytest.fixture
    def movie_dict(self, movie, director, genre):
        return {'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'trailer': movie.trailer,
                'year': movie.year,
                'rating': movie.rating,
                'genre': {'id': genre.id, 'name': genre.name},
                'director': {'id': director.id, 'name': director.name}}

    def test_many(self, client, movie, movie_dict):
        response = client.get('/movies/')
        assert response.status_code == 200
        assert response.json == [movie_dict]

    @pytest.mark.parametrize('page, answer', ([1, 1], [2, 0]), ids=["page one", "page two"])
    def test_movie_page(self, client, movie, page, answer):
        response = client.get(f'/movies/?page={page}')
        assert response.status_code == 200
        assert len(response.json) == answer

    def test_movie(self, client, movie, movie_dict):
        response = client.get('/movies/1/')
        assert response.status_code == 200
        assert response.json == movie_dict

    def test_movie_not_found(self, client, movie):
        response = client.get('/movies/2/')
        assert response.status_code == 404
