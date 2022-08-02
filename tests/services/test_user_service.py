from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound, BaseServiceError
from project.models import User
from project.services import UserService
from project.tools.security import generate_password_hash, generate_token


class TestUserService:
    @pytest.fixture
    def tokens(self, client, hash_password):
        return generate_token(data_user={'email': 'email1', 'password': hash_password})

    @pytest.fixture
    def invalid_token(self, client):
        return generate_token(data_user={'email': 'email1', 'password': 'password'})

    @pytest.fixture
    def hash_password(self, client):
        return generate_password_hash('test_password')

    @pytest.fixture
    @patch('project.dao.UserDAO')
    def user_dao_moc(self, moc_dao, hash_password):
        dao = moc_dao()
        dao.get_by_email.return_value = User(id=1,
                                             email='email1',
                                             password=hash_password,
                                             name='name1',
                                             surname='surname1',
                                             favorite_genre_id=1)
        return dao

    @pytest.fixture
    def user(self, db):
        item = User(email='email',
                    password="test_password",
                    name='name',
                    surname='surname',
                    favorite_genre_id=1)
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def user_update_data(self):
        return {'name': 'test_name',
                'surname': 'test_surname',
                'favourite_genre': 2}

    @pytest.fixture
    def user_service(self, user_dao_moc):
        return UserService(dao=user_dao_moc)

    @pytest.fixture
    def hash_password(self, user):
        return generate_password_hash(user.password)

    def test_get_by_email(self, user_service):
        assert user_service.get_by_email('test1')

    def test_user_not_found_by_email(self, user_service, user_dao_moc):
        user_dao_moc.get_by_email.return_value = None

        with pytest.raises(ItemNotFound):
            user_service.get_by_email('No_email')

    def test_profile_update(self, user, user_update_data, user_service):
        user_service.profile_update(user.email, user_update_data)
        item = user_service.get_by_email(user.email)
        assert item.name == user_update_data['name']
        assert item.surname == user_update_data['surname']
        assert item.favorite_genre_id == user_update_data['favourite_genre']

    def test_profile_update_raise(self, user, user_service, user_dao_moc):
        user_dao_moc.get_by_email.return_value = None

        with pytest.raises(BaseException):
            user_service.profile_update(user.email, {'test': None})

        with pytest.raises(ItemNotFound):
            user_service.profile_update(user.email, {'test': 'test'})

    def test_password_update(self, user, user_service):
        user_service.password_update(email=user.email, data={'old_password': 'test1', 'new_password': 'test2'})

    def test_password_raise(self, user, user_service, user_dao_moc):
        user_dao_moc.get_by_email.return_value = None
        with pytest.raises(BaseException):
            user_service.password_update(email=user.email, data={'old_password': 'test1', 'new_password': None})

        with pytest.raises(ItemNotFound):
            user_service.password_update(email=user.email, data={'old_password': 'test1', 'new_password': 'test2'})

    def test_add_user(self, user, user_service):
        user_service.add_user(data_user={'email': 'test1', 'password': 'test2'})
        assert user_service.get_by_email('test1')

    def test_add_user_raise(self, user, user_service):
        with pytest.raises(BaseException):
            user_service.add_user(data_user={"test": None})

    def test_user_password_verification(self, user, user_service):
        user_service.user_password_verification(data_user={'email': user.email, 'password': user.password})

    def test_user_password_verification_raise(self, user, user_service):
        with pytest.raises(BaseServiceError):
            user_service.user_password_verification(data_user={'email': user.email, 'password': None})

        with pytest.raises(BaseServiceError):
            user_service.user_password_verification(data_user={'email': user.email, 'password': 'not_password'})

    def test_generate_new_token(self, tokens, user_service, user):
        tokens = user_service.generate_new_token(tokens['refresh_token'])
        assert len(tokens.values()) == 2

    def test_generate_new_token_raise(self, invalid_token, user, user_service):
        with pytest.raises(BaseException):
            user_service.generate_new_token(token='')

        with pytest.raises(BaseException):
            user_service.generate_new_token(token=invalid_token['refresh_token'])
