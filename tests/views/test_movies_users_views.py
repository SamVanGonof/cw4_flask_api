import pytest

from project.models import User, Movie, Genre, Director
from project.tools.security import generate_token


class TestMovieUserView:
    @pytest.fixture
    def tokens(self, client):
        return generate_token(data_user={'email': 'email', 'password': 'test_password'})

    @pytest.fixture
    def director(self, db):
        item = Director(name='director')
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def movie1(self, db, genre, director):
        item = Movie(title='movie1',
                     description='description1',
                     trailer='trailer1',
                     year=1000,
                     rating=1.1,
                     genre=genre,
                     director=director)
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def movie2(self, db, genre, director):
        item = Movie(title='movie2',
                     description='description2',
                     trailer='trailer2',
                     year=2000,
                     rating=2.2,
                     genre=genre,
                     director=director)
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def genre(self, db):
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        return obj

    @pytest.fixture
    def user(self, db, movie1, genre):
        item = User(email='email',
                    password="test_password",
                    name='name',
                    surname='surname',
                    favorite_genre=genre,
                    movie_favorites=[movie1])
        db.session.add(item)
        db.session.commit()
        return item

    def test_get_favorite_movie(self, client, user, tokens, movie1, genre, director):
        client.set_cookie('localhost', 'AccessToken', tokens['access_token'])
        response = client.get('/favorites/movies/')
        assert response.status_code == 200
        assert response.json == [{'id': movie1.id,
                                  'title': movie1.title,
                                  'description': movie1.description,
                                  'trailer': movie1.trailer,
                                  'year': movie1.year,
                                  'rating': movie1.rating,
                                  'genre': {'id': genre.id, 'name': genre.name},
                                  'director': {'id': director.id, 'name': director.name}}]

    def test_get_favorite_movie_not_token(self, client, user):
        response = client.get('/favorites/movies/')
        assert response.status_code == 401

    def test_get_favorite_movie_add(self, client, user, tokens, movie1, movie2, genre, director):
        client.set_cookie('localhost', 'AccessToken', tokens['access_token'])
        response = client.post('favorites/movies/2/')
        movies = client.get('/favorites/movies/').json
        assert response.status_code == 200
        assert len(movies) == 2

    def test_get_favorite_movie_delete(self, client, user, tokens, movie1, movie2, genre, director):
        client.set_cookie('localhost', 'AccessToken', tokens['access_token'])
        response = client.delete('favorites/movies/1/')
        movies = client.get('/favorites/movies/').json
        assert response.status_code == 200
        assert len(movies) == 0
