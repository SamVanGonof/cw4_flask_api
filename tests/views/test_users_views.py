import pytest

from project.models import User
from project.tools.security import generate_token, generate_password_hash


class TestUser:
    @pytest.fixture
    def tokens(self, client, user):
        return generate_token(data_user={'email': user.email, 'password': user.password})

    @pytest.fixture
    def invalid_tokens(self, client, user):
        return generate_token(data_user={'email': 'no_email', 'password': user.password})

    @pytest.fixture
    def hash_password(self, client):
        return generate_password_hash('test_password')

    @pytest.fixture
    def user(self, db, hash_password):
        item = User(email='email',
                    password=hash_password,
                    name='name',
                    surname='surname',
                    favorite_genre_id=1)
        db.session.add(item)
        db.session.commit()
        return item

    def test_get_user(self, client, user, tokens):
        client.set_cookie('localhost', key='AccessToken', value=tokens['access_token'])
        response = client.get('/user/')
        assert response.status_code == 200

    def test_get_user_raise(self, client, user, invalid_tokens):
        client.set_cookie('localhost', key='AccessToken', value=invalid_tokens['access_token'])
        response = client.get('/user/')
        assert response.status_code == 404

    def test_profile_update(self, client, user, tokens):
        client.set_cookie('localhost', key='AccessToken', value=tokens['access_token'])
        response = client.patch('/user/', json={'name': 'test_name', 'surname': 'surname_test', 'favourite_genre': 2})
        user = client.get('/user/').json
        assert response.status_code == 200
        assert user['name'] == 'test_name'
        assert user['surname'] == 'surname_test'

    def test_profile_update_raise(self, client, user, tokens):
        client.set_cookie('localhost', key='AccessToken', value=tokens['access_token'])
        response = client.patch('/user/', json={'name': '', 'surname': '', 'favourite_genre': 0})
        assert response.status_code == 500

    def test_update_password_user(self, client, user, tokens):
        client.set_cookie('localhost', key='AccessToken', value=tokens['access_token'])
        response = client.put('/user/password/', json={'old_password': 'test_password',
                                                       'new_password': 'test_password_update'})
        assert response.status_code == 200

    def test_update_password_user_raise(self, client, user, tokens):
        client.set_cookie('localhost', key='AccessToken', value=tokens['access_token'])
        response = client.put('/user/password/', json={'old_password': '',
                                                       'new_password': ''})
        assert response.status_code == 500


