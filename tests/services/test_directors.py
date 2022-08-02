import pytest
from unittest.mock import patch

from project.exceptions import ItemNotFound
from project.models import Director
from project.services import DirectorsService


class TestDirectorService:
    @pytest.fixture
    @patch('project.dao.DirectorDAO')
    def director_dao_moc(self, moc_dao):
        dao = moc_dao()
        dao.get_by_id.return_value = Director(id=1, name="Director")
        dao.get_all.return_value = [Director(id=1, name="Director1"),
                                    Director(id=2, name="Director2")]
        return dao

    @pytest.fixture
    def director_service(self, director_dao_moc):
        return DirectorsService(dao=director_dao_moc)

    @pytest.fixture
    def director(self, db):
        item = Director(name='Director_test')
        db.session.add(item)
        db.session.commit()
        return item

    def test_get_director(self, director_service, director):
        assert director_service.get_item(director.id)

    def test_director_not_found(self, director_dao_moc, director_service):
        director_dao_moc.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            director_service.get_item(10)

    @pytest.mark.parametrize("page", [1, None], ids=['with page', 'without page'])
    def test_get_directors(self, director_dao_moc, director_service, page):
        directors = director_service.get_all(page=page)
        assert len(directors) == 2
        assert directors == director_dao_moc.get_all.return_value
        director_dao_moc.get_all.assert_called_with(page=page)

