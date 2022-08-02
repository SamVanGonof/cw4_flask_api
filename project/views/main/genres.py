from flask_restx import Namespace, Resource

from project.container import genre_service
from project.setup.api.models import genre
from project.setup.api.parsers import pr_page

api = Namespace('genres')


@api.route('/')
class GenresView(Resource):
    @api.expect(pr_page)
    @api.marshal_with(genre, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all genres.
        """
        return genre_service.get_all(**pr_page.parse_args())


@api.route('/<int:genre_id>/')
class GenreView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(genre, code=200, description='OK')
    def get(self, genre_id: int):
        """
        Get genre by id.
        """
        return genre_service.get_item(genre_id)
