import pytest

from project.models import User
from project.tools.security import generate_password_hash, generate_token


class TestAuth:
    @pytest.fixture
    def tokens(self, client, user):
        return generate_token(data_user={'email': user.email, 'password': user.password})

    @pytest.fixture
    def hash_password(self, client):
        return generate_password_hash('test_password')

    @pytest.fixture
    def user(self, db, hash_password):
        item = User(email='email',
                    password=hash_password,
                    name='name',
                    surname='surname')
        db.session.add(item)
        db.session.commit()
        return item

    def test_register_new_user(self, client):
        response = client.post('/auth/register/', json={'email': 'email', 'password': 'password'})
        assert response.status_code == 200

    def test_register_new_user_raise(self, client, user):
        response = client.post('/auth/register', json={'email': 'email', 'password': None})
        assert response.status_code == 308

    def test_get_token(self, client, user):
        response = client.post('/auth/login/', json={'email': user.email, 'password': 'test_password'})
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_get_token_raise(self, client, user):
        response = client.post('/auth/login/', json={'email': user.email, 'password': ''})
        assert response.status_code == 500

    def test_update_token_by_refresh_token(self, client, user, tokens):
        client.set_cookie('localhost', key='RefreshToken', value=tokens['refresh_token'])
        response = client.put('/auth/login/')
        assert response.status_code == 200
        assert len(response.json) == 2
