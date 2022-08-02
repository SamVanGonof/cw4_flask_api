import pytest

from project.dao import DirectorDAO
from project.models import Director


class TestDirector:
    @pytest.fixture
    def dao_director(self, db):
        return DirectorDAO(db.session)

    @pytest.fixture
    def director1(self, db):
        item = Director(name='Квентин')
        db.session.add(item)
        db.session.commit()
        return item

    @pytest.fixture
    def director2(self, db):
        item = Director(name='Scott')
        db.session.add(item)
        db.session.commit()
        return item

    def test_get_by_id(self, dao_director, director1):
        assert dao_director.get_by_id(director1.id) == director1

    def test_get_director_by_id_not_found(self, dao_director):
        assert not dao_director.get_by_id(1)

    def test_get_all_genres(self, dao_director, director1, director2):
        assert dao_director.get_all() == [director1, director2]

    def test_get_genres_by_page(self, dao_director, director1, director2, app):
        app.config['ITEMS_PER_PAGE'] = 1
        assert dao_director.get_all(1) == [director1]
        assert dao_director.get_all(2) == [director2]
        assert dao_director.get_all(3) == []




