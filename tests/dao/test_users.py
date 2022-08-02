import pytest

from project.dao import UserDAO
from project.models import User


class TestUsers:
    @pytest.fixture
    def dao_user(self, db):
        return UserDAO(db.session)

    @pytest.fixture
    def user1(self, db):
        item = User(email='email1',
                    password='password1')
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def user2(self, db):
        item = User(email='email2',
                    password='password2')
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def user3(self):
        return {"email": 'email3',
                "password": 'password3'}

    def test_get_user_by_id(self, user1, dao_user):
        assert dao_user.get_by_id(user1.id) == user1

    def test_get_user_by_id_not_found(self, dao_user):
        assert not dao_user.get_by_id(1)

    def test_get_all_users(self, dao_user, user1, user2):
        assert dao_user.get_all() == [user1, user2]

    def test_get_users_by_page(self, app, dao_user, user1, user2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert dao_user.get_all(page=1) == [user1]
        assert dao_user.get_all(page=2) == [user2]
        assert dao_user.get_all(page=3) == []

    def test_get_by_email(self, dao_user, user1, user2):
        assert dao_user.get_by_email('email1') == user1

    def test_add_user(self, dao_user, user3):
        dao_user.add_user(user3)
        user = dao_user.get_by_email(user3['email'])
        assert user

    def test_update_user(self, dao_user, user1, user2):
        user = dao_user.get_by_id(1)
        user.name = 'test'
        user.surname = 'test2'
        user.favorite_genre_id = 1
        dao_user.update(user)
        user_update = dao_user.get_by_id(1)
        assert user_update.name == 'test'
        assert user_update.surname == 'test2'
        assert user_update.favorite_genre_id == 1
