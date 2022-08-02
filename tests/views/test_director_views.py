import pytest

from project.models import Director


class TestDirectorViews:
    @pytest.fixture
    def director(self, db):
        item = Director(name='director')
        db.session.add(item)
        db.session.commit()
        return item

    def test_many(self, client, director):
        response = client.get('/directors/')
        assert response.status_code == 200
        assert response.json == [{"id": director.id, "name": director.name}]

    @pytest.mark.parametrize('page, answer', ([1, 1], [2, 0]), ids=["page one", "page two"])
    def test_director_page(self, client, director, page, answer):
        response = client.get(f'/directors/?page={page}')
        assert response.status_code == 200
        assert len(response.json) == answer

    def test_director(self, client, director):
        response = client.get('/directors/1/')
        assert response.status_code == 200
        assert response.json == {"id": director.id, "name": director.name}

    def test_genre_not_found(self, client, director):
        response = client.get('/directors/2/')
        assert response.status_code == 404


